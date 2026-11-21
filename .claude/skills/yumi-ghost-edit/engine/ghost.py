#!/usr/bin/env python3
"""玉米講鬼 renderer (16:9 host show with escalating horror).

usage: python3 -I ghost.py edl.json out.mp4 [--stills t1,t2]

EDL:
{
  "audio": "narration.wav (48k mono)", "transcript": "transcript.json",
  "assets": {"room": "...", "desk": "...", "sprites": "dir with v_closed.png ..."},
  "blocks": [
    {"src": [[a,b],...] | "gap": seconds,          # narration ranges (source sec) or silence
     "max_pause": 0.45,                            # silences longer than this are shortened to it
     "mode": "host" | "broll" | "black",
     "light": 0.0..1.0,                            # 0 warm studio, 1 pitch dark
     "zoom": [z0, z1],                             # host camera push (1 = wide)
     "broll": {"file": "...", "start": 0},         # for mode broll
     "pip": true,                                  # mascot window during broll/black
     "cards": [{"src_t": 471.5 | "t": 0.2 (block-local), "lines": [["你看我", "w"], ["像神？", "r"]], "hold": "block"}],
     "title": {"line1": "...", "line2": "...", "strip": "..."},
     "trans": "cut" | "flicker" | "flash" | "fade",
     "sfx": [{"t": 0.0 | "src_t": 569.1, "kind": "hit", "db": 0}],
     "dread": 0..1                                 # drone / wind level
    }, ...],
  "fixes": {"wrong": "right", ...}
}
"""
import json, os, subprocess, sys, tempfile
import numpy as np, cv2
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfx, audio, lipsync, render, foley  # noqa: E402

W, H, FPS, SR = 1920, 1080, 30, 48000
rng = np.random.default_rng(11)


# ============================================================ timeline
def silent_runs(x, a, b, thr_db=-38, hop=0.02):
    """Return [(s,e)] silences (source sec) inside [a,b]."""
    i0, i1 = int(a * SR), int(b * SR)
    seg = x[i0:i1]
    h = int(hop * SR)
    n = len(seg) // h
    if n == 0:
        return []
    db = 20 * np.log10(np.sqrt((seg[:n * h].reshape(n, h) ** 2).mean(1)) + 1e-9)
    sil = db < thr_db
    runs, s = [], None
    for k, v in enumerate(sil):
        if v and s is None:
            s = k
        if (not v or k == n - 1) and s is not None:
            e = k if not v else k + 1
            runs.append((a + s * hop, a + e * hop)); s = None
    return runs


def compress(x, a, b, max_pause):
    """Split [a,b] into kept pieces so no silence exceeds max_pause."""
    pieces, cur = [], a
    for s, e in silent_runs(x, a, b):
        if e - s > max_pause:
            keep = max_pause / 2
            pieces.append((cur, s + keep)); cur = e - keep
    pieces.append((cur, b))
    return [(p, q) for p, q in pieces if q - p > 0.03]


class Timeline:
    def __init__(self, edl, voice):
        self.blocks = edl["blocks"]
        self.pieces = []  # (out_t0, src_a, src_b, block_idx)
        t = 0.0
        for bi, bl in enumerate(self.blocks):
            bl["t0"] = t
            if "gap" in bl:
                t += bl["gap"]
            else:
                for a, b in bl["src"]:
                    for p, q in compress(voice, a, b, bl.get("max_pause", 0.45)):
                        self.pieces.append((t, p, q, bi)); t += q - p
            bl["t1"] = t
        self.dur = t
        self.n = int(round(t * FPS))

    def src2out(self, s, bi=None):
        ps = [p for p in self.pieces if bi is None or p[3] == bi]
        for t0, a, b, _ in ps:
            if a <= s <= b:
                return t0 + s - a
        best = None
        for t0, a, b, _ in ps:  # nearest kept point
            d = min(abs(s - a), abs(s - b))
            if best is None or d < best[0]:
                best = (d, t0 if abs(s - a) < abs(s - b) else t0 + b - a)
        return best[1] if best else 0.0

    def block_at(self, t):
        for i, bl in enumerate(self.blocks):
            if bl["t0"] <= t < bl["t1"]:
                return i, bl
        return len(self.blocks) - 1, self.blocks[-1]


# ============================================================ subtitles
def subtitle_lines(edl, tl, maxc=14):
    """Phrase-based subtitles: one whisper segment = one line, long ones split near the middle at word boundaries."""
    tr = json.load(open(edl["transcript"]))
    fixes = sorted(edl.get("fixes", {}).items(), key=lambda kv: -len(kv[0]))
    nosub = [r for bl in tl.blocks for r in bl.get("nosub", [])]
    def fix(t):
        for k, v in fixes:
            t = t.replace(k, v)
        return t.strip("，。,.、？?！!：: ")
    out = []
    for bi, bl in enumerate(tl.blocks):
        if "gap" in bl:
            continue
        pcs = [p for p in tl.pieces if p[3] == bi]
        def kept_word(w):
            mid = (w["s"] + w["e"]) / 2
            if any(a_ <= mid <= b_ for a_, b_ in nosub):
                return False
            return any(a_ - 0.05 <= mid <= b_ + 0.05 for _, a_, b_, _ in pcs)
        m = lambda x: tl.src2out(x, bi)
        for seg in tr:
            ws = [w for w in seg["words"] if w["w"].strip() and kept_word(w)]
            groups, cur = [], []
            for w in ws:
                if cur and (w["s"] - cur[-1]["e"] > 0.6 or abs((m(w["s"]) - m(cur[-1]["e"])) - (w["s"] - cur[-1]["e"])) > 0.3):
                    groups.append(cur); cur = []
                cur.append(w)
            if cur:
                groups.append(cur)
            for g in groups:
                text = "".join(w["w"].strip() for w in g)
                n = max(1, int(np.ceil(len(text) / maxc)))
                if n == 1:
                    chunks = [g]
                else:
                    chunks, acc, target = [], [], len(text) / n
                    for w in g:
                        acc.append(w)
                        if len("".join(x["w"].strip() for x in acc)) >= target and len(chunks) < n - 1:
                            chunks.append(acc); acc = []
                    if acc:
                        chunks.append(acc)
                for ch in chunks:
                    t = fix("".join(w["w"].strip() for w in ch))
                    if not t:
                        continue
                    t0 = m(ch[0]["s"]); t1 = min(m(ch[-1]["e"]) + 0.2, bl["t1"])
                    out.append([t0, max(t1, t0 + 0.7), t])
    out.sort()
    for i in range(len(out) - 1):
        if out[i + 1][0] - out[i][1] < 0.3:
            out[i][1] = out[i + 1][0]
        out[i][1] = min(out[i][1], out[i + 1][0])
    return out


def sub_layer(text):
    f = gfx.font(gfx.TC_SANS, 58)
    mask = gfx.text_mask(text, f, tracking=3)
    img = gfx.solid(mask, (244, 242, 236))
    a = mask.filter(__import__("PIL.ImageFilter", fromlist=["x"]).MaxFilter(7))
    edge = gfx.solid(a, (10, 8, 10), 235)
    pad = 6
    out = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    out.alpha_composite(edge, (pad - 3, pad - 3) if False else (pad, pad))
    out.alpha_composite(img, (pad, pad))
    out = gfx.shadowed(out, 6, (0, 4), 200)
    return gfx.to_layer(out, W / 2, H - 92)


# ============================================================ graphics
def distressed(text, size, color, seed, serif=True):
    f = gfx.font(gfx.TC_SERIF if serif else gfx.TC_SANS, size)
    m = gfx.text_mask(text, f, tracking=int(size * 0.05))
    m = gfx.skew(m, -0.05)
    a = np.array(m, np.float32) / 255
    r = np.random.default_rng(seed)
    blot = cv2.GaussianBlur(r.random(a.shape).astype(np.float32), (0, 0), size / 40)
    blot = (blot - blot.min()) / (blot.max() - blot.min() + 1e-6)
    streak = cv2.resize(r.random((max(2, a.shape[0] // 3), max(2, a.shape[1] // 40))).astype(np.float32),
                        (a.shape[1], a.shape[0]), interpolation=cv2.INTER_LINEAR)
    a = a * np.clip((blot - 0.12) * 6, 0, 1) * np.clip((streak - 0.04) * 6, 0, 1)
    edge_noise = cv2.GaussianBlur(r.random(a.shape).astype(np.float32), (0, 0), 1.2)
    a = np.clip(a * (0.75 + 0.5 * edge_noise), 0, 1)
    img = Image.new("RGBA", (a.shape[1], a.shape[0]), color + (0,))
    img.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    return img


def card_image(lines, seed=0):
    rows = []
    for i, (txt, col) in enumerate(lines):
        c = (240, 236, 228) if col == "w" else (232, 34, 38)
        im = distressed(txt, 132 if len(txt) <= 6 else 108, c, seed + i)
        if col == "r":
            im = gfx.glow(im, 20, (255, 40, 40), 150)
        rows.append(gfx.shadowed(im, 12, (0, 8), 230))
    w = max(r.width for r in rows); h = sum(r.height for r in rows) - 40 * (len(rows) - 1)
    pad = 120
    out = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    back = Image.new("L", out.size, 0)
    ImageDraw.Draw(back).ellipse([(pad // 2, pad // 2), (out.width - pad // 2, out.height - pad // 2)], fill=150)
    back = back.filter(__import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(50))
    out.alpha_composite(gfx.solid(back, (0, 0, 0)))
    y = pad
    for r in rows:
        out.alpha_composite(r, (pad + (w - r.width) // 2, y)); y += r.height - 40
    return np.array(out).astype(np.float32)


def title_image(line1, line2, strip):
    t1 = gfx.shadowed(distressed(line1, 210, (238, 236, 230), 101), 14, (0, 10), 240)
    t2 = gfx.shadowed(gfx.glow(distressed(line2, 170, (204, 16, 22), 202), 22, (255, 20, 20), 120), 14, (0, 10), 240)
    w = max(t1.width, t2.width)
    out = Image.new("RGBA", (w, t1.height + t2.height + 40), (0, 0, 0, 0))
    out.alpha_composite(t1, ((w - t1.width) // 2, 0)); out.alpha_composite(t2, ((w - t2.width) // 2, t1.height - 90))
    if strip:
        s = Image.new("RGBA", (820, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
        d.polygon([(12, 10), (812, 0), (804, 88), (0, 96)], fill=(198, 152, 72, 240))
        st = gfx.solid(gfx.text_mask(strip, gfx.font(gfx.TC_SERIF, 56), 8), (34, 22, 12))
        s.alpha_composite(st, ((820 - st.width) // 2, (96 - st.height) // 2))
        out.alpha_composite(s, ((w - 820) // 2, t1.height + t2.height - 130))
    return np.array(out).astype(np.float32)


def channel_tag():
    a = gfx.solid(gfx.text_mask("玉米講鬼", gfx.font(gfx.TC_SERIF, 46), 4), (236, 232, 224))
    b = gfx.solid(gfx.text_mask("TALK", gfx.font(gfx.EN_B, 30), 4), (210, 30, 34))
    c = gfx.solid(gfx.text_mask("民間怪談系列", gfx.font(gfx.TC_SANS, 24), 4), (236, 232, 224))
    out = Image.new("RGBA", (max(a.width + b.width + 14, c.width + 30), a.height + c.height + 26), (0, 0, 0, 0))
    out.alpha_composite(a, (0, 0)); out.alpha_composite(b, (a.width + 10, a.height - b.height - 4))
    d = ImageDraw.Draw(out); d.rectangle([(0, a.height + 6), (c.width + 24, a.height + c.height + 22)], fill=(150, 14, 18, 230))
    out.alpha_composite(c, (12, a.height + 12))
    return np.array(gfx.shadowed(out, 6, (0, 3), 200)).astype(np.float32)


def over(dst, s, x, y, amul=1.0):
    h, w_ = s.shape[:2]; x0, y0 = max(x, 0), max(y, 0); x1, y1 = min(dst.shape[1], x + w_), min(dst.shape[0], y + h)
    if x1 <= x0 or y1 <= y0 or amul <= 0:
        return
    p = s[y0 - y:y1 - y, x0 - x:x1 - x]; a = p[..., 3:4] / 255 * amul
    r = dst[y0:y1, x0:x1]; r *= (1 - a); r += p[..., :3] * a


def scale(img, k):
    return cv2.resize(img, (max(1, int(img.shape[1] * k)), max(1, int(img.shape[0] * k))), interpolation=cv2.INTER_CUBIC)


# ============================================================ audio
def drone(n, seed=4):
    t = np.arange(n) / SR
    r = np.random.default_rng(seed)
    x = np.zeros(n)
    for f, a in ((43.65, 1), (46.25, 0.7), (65.4, 0.5), (69.3, 0.35), (98, 0.18), (103.8, 0.12)):
        lfo = 0.6 + 0.4 * np.sin(2 * np.pi * (0.05 + r.random() * 0.07) * t + r.random() * 6)
        x += a * lfo * np.sin(2 * np.pi * f * t + r.random() * 6)
    air = audio.bp(r.standard_normal(n), 300, 900) * 0.15 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t))
    return (x + air) / 3


def wind(n, seed=5):
    r = np.random.default_rng(seed); t = np.arange(n) / SR
    x = audio.bp(r.standard_normal(n), 200, 1400)
    gust = 0.35 + 0.65 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.13 * t)) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.31 * t + 1))
    return x * gust * 0.5


def heartbeat(n, bpm=62):
    out = np.zeros(n); beat = int(60 / bpm * SR); L = int(0.25 * SR); t = np.arange(L) / SR
    thump = np.sin(2 * np.pi * 52 * t) * np.exp(-t * 26)
    for s in range(0, n, beat):
        for off, g in ((0, 1.0), (int(0.22 * SR), 0.7)):
            i = s + off
            if i + L < n:
                out[i:i + L] += thump * g
    return out


def stinger():
    L = int(1.6 * SR); t = np.arange(L) / SR
    x = sum(np.sin(2 * np.pi * f * t) for f in (311, 330, 466, 494, 698))
    x = x * np.exp(-t * 2.2) + audio.hp(np.random.default_rng(1).standard_normal(L), 3000) * np.exp(-t * 8) * 0.6
    return x / 4


SFX_FILES = {}
_wav_cache = {}


def load_mono(path):
    if path not in _wav_cache:
        _wav_cache[path] = render.read_wav(path).mean(1).astype(np.float64)
    return _wav_cache[path]


def looped(path, n):
    x = load_mono(path)
    reps = int(np.ceil(n / len(x)))
    return np.tile(x, reps)[:n]


def ghost_sfx(kind):
    if kind in SFX_FILES:
        return load_mono(SFX_FILES[kind]).copy()
    if kind in foley.ONESHOTS:
        return foley.ONESHOTS[kind]()
    if kind == "stinger":
        return stinger()
    if kind == "buzz":
        L = int(0.5 * SR); t = np.arange(L) / SR
        return np.sign(np.sin(2 * np.pi * 120 * t)) * (np.random.default_rng(2).random(L) > 0.3) * 0.25 * np.exp(-t * 3)
    return audio.sfx(kind)


def movavg(x, k):
    """O(n) centred moving average (np.convolve with a long box kernel is O(n*k))."""
    k = max(1, int(k)); c = np.cumsum(np.concatenate([[0.0], np.asarray(x, np.float64)]))
    n = len(x); i = np.arange(n); lo = np.clip(i - k // 2, 0, n); hi = np.clip(i - k // 2 + k, 0, n)
    return (c[hi] - c[lo]) / np.maximum(hi - lo, 1)


def build_audio(edl, tl, voice, tmp):
    SFX_FILES.update(edl.get("sfx_files", {}))
    n = int(tl.dur * SR) + SR
    v = np.zeros(n)
    fade = int(0.008 * SR)
    for t0, a, b, _ in tl.pieces:
        seg = voice[int(a * SR):int(b * SR)].copy()
        if len(seg) > 2 * fade:
            seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
        i = int(t0 * SR); v[i:i + len(seg)] += seg
    vin = os.path.join(tmp, "v.wav"); vout = os.path.join(tmp, "v2.wav")
    render.write_wav(vin, v[:, None])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vin, "-af",
                    "highpass=f=70,acompressor=threshold=-24dB:ratio=2.5:attack=8:release=200:makeup=3", vout], check=True)
    v = render.read_wav(vout)[:, 0][:n]
    if len(v) < n:
        v = np.pad(v, (0, n - len(v)))
    e = audio.rms_env(v); act = 20 * np.log10(e + 1e-12) > -38
    speech = np.median(e[act]) if act.any() else 0.05
    # dread envelope per sample from blocks
    dread = np.zeros(n)
    for bl in tl.blocks:
        dread[int(bl["t0"] * SR):int(bl["t1"] * SR)] = bl.get("dread", bl.get("light", 0))
    dread = movavg(dread, int(0.8 * SR))
    duck = audio.duck_gain(v, 5)
    def env_from(key, default=None):
        e_ = np.full(n, np.nan)
        for bl in tl.blocks:
            val = bl.get(key, default)
            if val is not None:
                e_[int(bl["t0"] * SR):int(bl["t1"] * SR)] = val
        return e_
    def smooth(x, secs=0.6):
        return movavg(x, int(secs * SR))
    bed = np.zeros(n)
    if edl.get("music"):
        mw = render.read_wav(edl["music"])[:, 0].astype(np.float64)
        mw = mw / (np.sqrt(np.mean(mw ** 2)) + 1e-9)
        # walk blocks: continue the track, jump (with crossfade) where a block sets music_at
        cur = 0; xf = int(1.0 * SR); bls = tl.blocks
        for k, bl in enumerate(bls):
            i0, i1 = int(bl["t0"] * SR), min(n, int(bl["t1"] * SR))
            if "music_at" in bl:
                cur = int(bl["music_at"] * SR)
            L = i1 - i0
            tail = xf if (k + 1 < len(bls) and "music_at" in bls[k + 1]) else 0
            seg = mw[(cur + np.arange(L + tail)) % len(mw)].copy()
            xin = min(xf, len(seg))  # blocks can be shorter than the crossfade after cut_edl
            if "music_at" in bl and k > 0 and xin > 1:
                seg[:xin] *= np.linspace(0, 1, xin)
            if tail:
                seg[-tail:] *= np.linspace(1, 0, tail)
            m_ = min(len(seg), n - i0)
            bed[i0:i0 + m_] += seg[:m_]
            cur += L
        mlev = smooth(np.nan_to_num(env_from("music_db"), nan=-20.0))  # dB relative to speech
        bed = bed * speech * audio.db(mlev) * duck
    dl = np.clip(dread - 0.55, 0, 1) * 2
    dr = drone(n); bed += dr / (np.sqrt(np.mean(dr ** 2)) + 1e-9) * speech * audio.db(-26) * dl * duck
    # ambience beds
    for name, fn in foley.BEDS.items():
        lev = env_from("amb_" + name)
        if np.all(np.isnan(lev)):
            continue
        g = smooth(np.where(np.isnan(lev), 0, audio.db(np.nan_to_num(lev, nan=-90))), 0.8)
        bf = edl.get("bed_files", {}).get(name)
        x = looped(bf, n) if bf else fn(n)
        x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9)
        bed += x * speech * g * (0.55 + 0.45 * duck)
    hb = np.zeros(n)
    for bl in tl.blocks:
        if bl.get("heartbeat"):
            i0, i1 = int(bl["t0"] * SR), int(bl["t1"] * SR)
            h = looped(edl["heartbeat_file"], i1 - i0) if edl.get("heartbeat_file") else heartbeat(i1 - i0, bl.get("heartbeat_bpm", 64))
            hb[i0:i1] += h / (np.sqrt(np.mean(h ** 2)) + 1e-9) * speech * audio.db(-14)
    mix = v + bed + hb
    for bi_, bl in enumerate(tl.blocks):
        for s in bl.get("sfx", []):
            t = bl["t0"] + s["t"] if "t" in s else tl.src2out(s["src_t"], bi_)
            x = ghost_sfx(s["kind"])
            if s.get("dur"):
                m_ = int(s["dur"] * SR)
                if len(x) > m_:
                    x = x[:m_].copy(); f_ = min(int(0.4 * SR), m_ // 3); x[-f_:] *= np.linspace(1, 0, f_)
            x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * speech * audio.db(-8 + s.get("db", 0))
            i = int(t * SR); L = min(len(x), n - i)
            if L > 0:
                mix[i:i + L] += x[:L]
    mix = mix[:int(tl.dur * SR)]
    tail = int(0.6 * SR); mix[-tail:] *= np.linspace(1, 0, tail)
    pre = os.path.join(tmp, "pre.wav"); fin = os.path.join(tmp, "mix.wav")
    render.write_wav(pre, np.stack([mix, mix], 1) * 0.5)
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", pre, "-af", "loudnorm=I=-14:TP=-2:LRA=14:print_format=json",
                           "-f", "null", "-"], capture_output=True, text=True).stderr
    js = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af",
                    f"loudnorm=I=-14:TP=-2:LRA=14:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
                    f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true",
                    "-ar", str(SR), fin], check=True)
    return fin, v


# ============================================================ video
class BrollReader:
    def __init__(self, f, start, dur, speed=1.0, loop=True):
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):  # still image -> the shot's own push/pan animates it
            self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-i", f,
                                       "-t", f"{dur + 0.5:.2f}", "-vf",
                                       f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                                       "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
            self.last = np.zeros((H, W, 3), np.uint8)
            return
        if abs(speed - 1) > 1e-3:
            # slow motion: motion-compensated interpolation to a real 30 fps (no duplicated frames / judder);
            # interpolate at <=1280 px wide for speed, then scale up
            sp = (f"setpts=PTS/{speed:.4f},scale='min(1280,iw)':-2,"
                  f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,")
        else:
            sp = f"fps={FPS},"
        self.p = subprocess.Popen(["ffmpeg", "-v", "error"] + (["-stream_loop", "-1"] if loop else []) +
                                  ["-ss", f"{max(0.0, start):.3f}", "-i", f,
                                   "-t", f"{dur + 0.5:.2f}", "-vf",
                                   f"{sp}scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.last = np.zeros((H, W, 3), np.uint8)

    def read(self):
        b = self.p.stdout.read(W * H * 3)
        if len(b) == W * H * 3:
            self.last = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        return self.last

    def close(self):
        self.p.stdout.close(); self.p.kill(); self.p.wait()


def main():
    args = sys.argv[1:]
    edl = json.load(open(args[0])); out_path = args[1]
    stills = [float(x) for x in args[args.index("--stills") + 1].split(",")] if "--stills" in args else None
    rng_ = [float(x) for x in args[args.index("--range") + 1].split(",")] if "--range" in args else None
    video_only = "--video-only" in args
    audio_only = "--audio-only" in args
    import wave
    w = wave.open(edl["audio"]); voice = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    if w.getnchannels() > 1:
        voice = voice.reshape(-1, w.getnchannels()).mean(1)
    tl = Timeline(edl, voice)
    print(f"duration {tl.dur:.1f}s, {len(tl.pieces)} pieces", file=sys.stderr)

    # ---- assets
    A = edl["assets"]
    room = np.array(Image.open(A["room"]).convert("RGB")).astype(np.float32)
    ROOM = cv2.resize(room, (W, H), interpolation=cv2.INTER_CUBIC)
    ROOM = cv2.GaussianBlur(ROOM, (0, 0), 1.3)
    desk = np.array(Image.open(A["desk"])).astype(np.float32)
    DK = scale(desk, 0.98); SURF = 900; DKX, DKY = -330, SURF - int(490 * 0.98)
    SPR = {k: np.array(Image.open(os.path.join(A["sprites"], f"v_{k}.png"))).astype(np.float32)
           for k in ["closed", "half", "open", "wide", "o", "blink", "frown"] if os.path.exists(os.path.join(A["sprites"], f"v_{k}.png"))}
    EM = np.zeros((512, 512), np.float32)
    cv2.ellipse(EM, (190, 232), (54, 60), 0, 0, 360, 1, -1); cv2.ellipse(EM, (336, 242), (54, 60), 0, 0, 360, 1, -1)
    EM = cv2.GaussianBlur(EM, (0, 0), 3)[..., None]
    VIG = gfx.vignette((H, W), 0.75)[..., None].astype(np.float32)
    GRAIN = [(np.random.default_rng(i).standard_normal((H // 2, W // 2)).astype(np.float32)) for i in range(6)]
    GRAIN = [cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)[..., None] for g in GRAIN]
    TAG = channel_tag()
    PIP_D, PIP_C = 300, (W - 210, H - 300)
    yy, xx = np.mgrid[0:PIP_D, 0:PIP_D]
    CIRC = cv2.GaussianBlur((((xx - PIP_D / 2) ** 2 + (yy - PIP_D / 2) ** 2) <= (PIP_D / 2 - 2) ** 2).astype(np.float32), (3, 3), 0)[..., None]
    ring = Image.new("RGBA", (PIP_D + 80, PIP_D + 80), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse([(40, 40), (40 + PIP_D, 40 + PIP_D)], outline=(200, 30, 36, 255), width=6)
    RING = np.array(gfx.glow(ring, 14, (255, 40, 40), 120)).astype(np.float32)

    # ---- lip sync over whole timeline
    with tempfile.TemporaryDirectory() as tmp:
        mix_path, vproc = (None, None) if (stills or video_only) else build_audio(edl, tl, voice, tmp)
        if audio_only:
            import shutil; shutil.copy(mix_path, out_path); return
        # rms of the cut voice for gating
        vcut = np.zeros(int(tl.dur * SR) + SR)
        for t0, a, b, _ in tl.pieces:
            seg = voice[int(a * SR):int(b * SR)]; vcut[int(t0 * SR):int(t0 * SR) + len(seg)] = seg
        rms = lipsync.frame_rms_db(vcut, SR, FPS)
        tr = json.load(open(edl["transcript"]))
        allw = [x for s in tr for x in s["words"]]
        mouth = ["closed"] * tl.n
        for t0, a, b, _ in tl.pieces:
            ws = [dict(x) for x in allw if a - 0.05 <= (x["s"] + x["e"]) / 2 <= b + 0.05]
            f0, f1 = int(round(t0 * FPS)), min(tl.n, int(round((t0 + b - a) * FPS)))
            tk = lipsync.mouth_track(ws, tl.n, FPS, rms, offset=t0 - a)
            mouth[f0:f1] = tk[f0:f1]
        blinks = lipsync.blink_track(tl.n, FPS)

        # ---- per-block graphics
        cards = []  # (t0, t1, img)
        titles = []
        for bi, bl in enumerate(tl.blocks):
            for ci, c in enumerate(bl.get("cards", [])):
                t0 = bl["t0"] + c["t"] if "t" in c else tl.src2out(c["src_t"], bi)
                t1 = bl["t1"] if c.get("hold", "block") == "block" else t0 + c["hold"]
                cards.append((t0, t1, card_image(c["lines"], seed=bi * 10 + ci)))
            if "title" in bl:
                T = bl["title"]; titles.append((bl["t0"], bl["t1"], title_image(T["line1"], T["line2"], T.get("strip"))))
        sub_src = json.load(open(edl["subs_file"])) if edl.get("subs_file") else subtitle_lines(edl, tl)
        subs = [(a, b, sub_layer(t)) for a, b, t in sub_src]
        # ---- per-line shot list: [t_out, want, fallback]; want = Vecteezy file stem, fallback = clip name | host | black | None
        import glob as _glob
        vdir = edl.get("vecteezy_dir", ""); bdir = edl.get("broll_dir", "")
        reds = set(edl.get("red_clips", []))
        def resolve(want, fb):
            if want and vdir:
                hits = sorted(_glob.glob(os.path.join(vdir, want + "*")), key=lambda h: (not h.lower().endswith(".mp4"), h))
                if hits:
                    return ("broll", dict(file=hits[0], start=edl.get("vstart", {}).get(want, 0.5), red=False))
            if fb in ("host", "black"):
                return (fb, None)
            if fb:
                return ("broll", dict(file=os.path.join(bdir, fb + ".mp4"), start=edl.get("cstart", {}).get(fb, 0),
                                      red=fb in reds))
            return (None, None)
        SHOTS = []
        for k, sh in enumerate(sorted(edl.get("shots", []), key=lambda x: x[0])):
            m_, clip_ = resolve(sh[1], sh[2])
            SHOTS.append((sh[0], m_, clip_, k))
        n_used = sum(1 for sh in edl.get("shots", []) if sh[1] and resolve(sh[1], None)[0])
        print(f"shots: {len(SHOTS)}, vecteezy clips found for {n_used}", file=sys.stderr)
        # ---- no-repeat planner: every (shot, sub-shot) gets its own unused stretch of its clip.
        # When a clip is used up: 1st reuse = mirrored + punch-in variant, 2nd reuse = back to the host.
        _dur_cache = {}
        def clip_len(f):
            if f not in _dur_cache:
                r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                   capture_output=True, text=True).stdout.strip()
                _dur_cache[f] = 6.0 if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")) else float(r or 10)
            return _dur_cache[f]
        PLAN = {}   # shot index -> (clip start sec, playback speed)
        used = {}   # file -> [(a, b)] source seconds already shown
        MIN_SPEED = 0.45
        for i, (st0, m_, clip_, sk) in enumerate(SHOTS):
            if m_ != "broll":
                continue
            bi_, bl_ = tl.block_at(st0 + 0.01)
            if st0 < bl_["t0"] - 0.25:
                continue
            st1 = min(SHOTS[i + 1][0] if i + 1 < len(SHOTS) else tl.dur, bl_["t1"])
            need = max(st1 - st0, 1e-3) + 0.1
            f = clip_["file"]
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                PLAN[sk] = (0.0, 1.0); continue
            L_ = clip_len(f) - 0.05; base = min(clip_.get("start", 0), max(0.0, L_ - need))
            iv = sorted(used.get(f, []))
            def free_from(c0):  # length of unused source time starting at c0
                if any(a_ <= c0 < b_ for a_, b_ in iv):
                    return 0.0
                nxt = min([a_ for a_, b_ in iv if a_ > c0] + [L_])
                return max(0.0, nxt - c0)
            cands = sorted(set([base, 0.0] + [b_ for a_, b_ in iv]))
            best = max(cands, key=lambda c: (free_from(c) >= need, -c if free_from(c) >= need else free_from(c)))
            avail = free_from(best)
            if avail >= need:
                start, speed = best, 1.0                      # enough fresh footage: real time
            elif avail >= need * MIN_SPEED:
                start, speed = best, avail / need             # stretch the fresh footage (slow motion)
            else:                                             # clip used up: replay slowly, never loop/mirror
                print(f"  replay: {os.path.basename(f)} at {st0:.1f}s ({need:.1f}s needed)", file=sys.stderr)
                span = min(L_, need)
                speed = max(min(1.0, L_ / need), 0.2)
                start = max(0.0, min(base, L_ - need * speed))
            used.setdefault(f, []).append((start, start + need * speed))
            PLAN[sk] = (start, speed)
            if os.environ.get("PLAN_DEBUG"):
                print(f"  plan {st0:6.1f}-{st1:6.1f} {os.path.basename(f):28s} start {start:5.2f} speed {speed:.2f}", file=sys.stderr)
        n_slow = sum(1 for v in PLAN.values() if v[1] < 0.999)
        print(f"continuous plan: {len(PLAN)} shots, {n_slow} slowed down", file=sys.stderr)

        def shot_at(t, bl):
            cur = None
            for sh in SHOTS:
                if sh[0] <= t + 1e-6:
                    cur = sh
                else:
                    break
            if cur is None or cur[0] < bl["t0"] - 0.25 or cur[1] is None:
                return None
            nxt = next((sh[0] for sh in SHOTS if sh[0] > cur[0]), bl["t1"])
            return cur, min(nxt, bl["t1"])

        enc = None
        if not stills:
            if video_only:
                enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                                        "-pix_fmt", "yuv420p", out_path], stdin=subprocess.PIPE)
            else:
                enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                        "-r", str(FPS), "-i", "-", "-i", mix_path, "-map", "0:v", "-map", "1:a",
                                        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                                        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out_path],
                                       stdin=subprocess.PIPE)
        still_frames = sorted(int(round(s * FPS)) for s in stills) if stills else None
        readers = {}
        saved = []
        fa, fb = (int(round(rng_[0] * FPS)), min(tl.n, int(round(rng_[1] * FPS)))) if rng_ else (0, tl.n)
        key = None
        for fi in range(fa, fb):
            t = fi / FPS
            bi, bl = tl.block_at(t)
            if still_frames is not None and fi not in still_frames:
                continue
            lt = t - bl["t0"]; bd = max(bl["t1"] - bl["t0"], 1e-3); p = lt / bd
            L = bl.get("light", 0.0)
            # mascot sprite for this frame
            mk = mouth[fi]
            if L >= 0.4 and "frown" in SPR:  # dark parts: no grinning - talk with a scared "o", rest on a frown
                mk = {"closed": "frown", "half": "o", "open": "o", "wide": "o"}.get(mk, mk)
            c = SPR[mk].copy()
            if blinks[fi] and L < 0.85:
                c = c * (1 - EM) + SPR["blink"] * EM
            mode = bl.get("mode", "host")
            shot = None if bl.get("title") else shot_at(t, bl)
            plan = None
            if shot:
                mode = shot[0][1]

            if mode == "host":
                fr = ROOM.copy()
                s = 1.2 * (1 + 0.008 * np.sin(2 * np.pi * t / 3.2))
                im = scale(c, s)
                over(fr, im, 1010 - im.shape[1] // 2, SURF + 25 - im.shape[0] + int(4 * np.sin(2 * np.pi * t / 3.2)))
                over(fr, DK, DKX, DKY)
                z0, z1 = bl.get("zoom", [1.0, 1.04])
                z = z0 + (z1 - z0) * p
                if z > 1.001:
                    cx, cy = 1010, 560
                    M = np.float32([[z, 0, cx * (1 - z)], [0, z, cy * (1 - z)]])
                    fr = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
                # lighting: room darkens & cools, mascot keeps some monitor light
                if L > 0:
                    lum = fr.mean(2, keepdims=True)
                    fr = fr * (1 - 0.55 * L) + lum * 0.55 * L
                    fr *= (1 - 0.62 * L)
                    fr[..., 2] *= 1 + 0.18 * L; fr[..., 0] *= 1 - 0.08 * L
                    fr *= (1 - L * 0.6) + VIG * L * 0.6
            elif mode == "broll" and shot:
                (st0, _, clip, sk), st1 = shot
                ls = t - st0
                key = ("shot", sk)
                p0, speed = PLAN.get(sk, (clip.get("start", 0), 1.0))
                if key not in readers:
                    readers[key] = BrollReader(clip["file"], p0 + ls * speed, max(st1 - t, 0.1), speed, loop=False)
                fr = readers[key].read().astype(np.float32)
                sp = ls / max(st1 - st0, 1e-3)
                dirn = [(1.0, 1.07, 0.0), (1.08, 1.01, 0.0), (1.05, 1.05, 1.0), (1.05, 1.05, -1.0)][sk % 4]
                z = dirn[0] + (dirn[1] - dirn[0]) * sp; pan = dirn[2] * (sp - 0.5) * 50
                M = np.float32([[z, 0, W / 2 * (1 - z) + pan], [0, z, H / 2 * (1 - z)]])
                fr = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
                lum = fr.mean(2, keepdims=True); fr = fr * 0.35 + lum * 0.65
                fr *= (0.85 - 0.45 * L); fr[..., 0] *= 0.88; fr[..., 2] *= 1.12
                if clip.get("red"):
                    fr[..., 0] *= 1.35; fr[..., 1] *= 0.8; fr[..., 2] *= 0.8
                fr *= VIG
            elif mode == "broll":
                clips = bl.get("brolls") or [bl["broll"]]
                mx = bl.get("max_shot", 3.0)
                nshots = max(1, int(np.ceil(bd / mx))); slen = bd / nshots
                k = min(nshots - 1, int(lt / slen))
                clip = clips[k % len(clips)]
                key = (bi, k)
                if key not in readers:
                    st = clip.get("start", 0) + (k // len(clips)) * slen * 1.3 + (lt - k * slen)
                    readers[key] = BrollReader(clip["file"], st, slen + 0.2)
                fr = readers[key].read().astype(np.float32)
                sp = (lt - k * slen) / slen
                dirn = [(1.0, 1.08, 0.0), (1.1, 1.02, 0.0), (1.06, 1.06, 1.0), (1.06, 1.06, -1.0)][(bi + k) % 4]
                z = dirn[0] + (dirn[1] - dirn[0]) * sp
                pan = dirn[2] * (sp - 0.5) * 60
                M = np.float32([[z, 0, W / 2 * (1 - z) + pan], [0, z, H / 2 * (1 - z)]])
                fr = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
                red = clip.get("red", bl.get("broll", {}).get("red", False))
                lum = fr.mean(2, keepdims=True)
                fr = fr * 0.35 + lum * 0.65
                fr *= (0.85 - 0.45 * L)
                fr[..., 0] *= 0.88; fr[..., 2] *= 1.12
                if red:
                    fr[..., 0] *= 1.35; fr[..., 1] *= 0.8; fr[..., 2] *= 0.8
                fr *= VIG
            else:  # black
                fr = np.zeros((H, W, 3), np.float32)
            # grain everywhere it is dark-ish
            fr += GRAIN[fi % 6] * (5 + 9 * L)
            # pip mascot during broll/black
            if mode != "host" and bl.get("pip", True) and not bl.get("title"):
                face = c[110:450, 92:432]
                face = cv2.resize(face, (PIP_D, PIP_D), interpolation=cv2.INTER_AREA)
                x0, y0 = PIP_C[0] - PIP_D // 2, PIP_C[1] - PIP_D // 2
                reg = fr[y0:y0 + PIP_D, x0:x0 + PIP_D]
                bgc = np.array([28, 22, 30], np.float32) * (1 - 0.5 * L)
                inner = face[..., :3] * (face[..., 3:4] / 255) + bgc * (1 - face[..., 3:4] / 255)
                inner *= (1 - 0.35 * L)
                reg *= (1 - CIRC); reg += inner * CIRC
                over(fr, RING, PIP_C[0] - RING.shape[1] // 2, PIP_C[1] - RING.shape[0] // 2, 1.0)
            # titles & cards
            for t0, t1, img in titles:
                if t0 <= t < t1:
                    dt = t - t0
                    sh = (rng.normal(0, 16, 2) * max(0, 1 - dt / 0.35)).astype(int)
                    sc = 1.22 - 0.22 * min(1, dt / 0.12)
                    im = scale(img, sc * 0.82)
                    over(fr, im, W // 2 - im.shape[1] // 2 + sh[0], H // 2 - 40 - im.shape[0] // 2 + sh[1], min(1, dt / 0.05))
            for t0, t1, img in cards:
                if t0 <= t < t1:
                    dt = t - t0
                    flick = 1.0 if dt > 0.25 else (0.3 if rng.random() < 0.4 else 1.0)
                    sc = 1.08 - 0.08 * min(1, dt / 0.2)
                    im = scale(img, sc)
                    cx_ = 500 if mode == "host" else W // 2
                    over(fr, im, cx_ - im.shape[1] // 2, H // 2 - 70 - im.shape[0] // 2,
                         min(1, dt / 0.08) * flick * min(1, (t1 - t) / 0.15))
            # transitions into block
            tr_ = bl.get("trans", "cut")
            if tr_ == "flash" and lt < 0.12:
                a = 1 - lt / 0.12; fr = fr * (1 - a) + np.array([255, 245, 240]) * a
            elif tr_ == "flicker" and lt < 0.6 and rng.random() < 0.45:
                fr *= 0.15
            elif tr_ == "fade" and lt < 0.5:
                fr *= lt / 0.5
            if bl.get("fade_out") and bl["t1"] - t < 0.6:
                fr *= max(0, (bl["t1"] - t) / 0.6)
            if mode == "host" and not bl.get("title"):
                over(fr, TAG, 40, 30, 0.95)
            title_on = any(t0 <= t < t1 for t0, t1, _ in titles)
            if not title_on:
                for a, b, Ls in subs:
                    if a <= t < b:
                        over(fr, Ls.rgba.astype(np.float32), Ls.x, Ls.y)
            out = np.clip(fr, 0, 255).astype(np.uint8)
            if still_frames is not None:
                pth = os.path.splitext(out_path)[0] + f"_still_{t:07.2f}.jpg"
                Image.fromarray(out).save(pth, quality=88); saved.append(pth)
            else:
                enc.stdin.write(out.tobytes())
            # close finished readers
            for kk in [kk for kk in readers if kk != key]:
                readers.pop(kk).close()
        for r in readers.values():
            r.close()
        if enc:
            enc.stdin.close(); enc.wait()
    for s in saved:
        print(s)


if __name__ == "__main__":
    main()
