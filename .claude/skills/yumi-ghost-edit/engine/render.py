#!/usr/bin/env python3
"""Render a 9:16 explainer-style edit from an EDL json.

usage: python3 -I render.py edl.json out.mp4 [--preview] [--stills t1,t2,...]

EDL (times in SOURCE seconds unless key says otherwise):
{
  "source": "/abs/raw.mp4",
  "fps": 30,
  "shots": [ {"in": 6.1, "out": 11.3,
              "view": {"cx": 540, "cy": 960, "z0": 1.0, "z1": 1.05},   # crop centre (source px) + zoom start/end
              "plate": true,                 # dim + halftone + vignette (background for cards)
              "pip": {"cx": 238, "cy": 760, "size": 420},  # circular speaker window, top-right
              "trans": "cut" | "whip" | "flash" } ],
  "graphics": [ {"type": "intro|tag|gold_card|flow|metal_word", "t0": out_sec, "t1": out_sec | "end",
                 "src_t0"/"src_t1": alternative in source time, "args": {...}, "anim": "pop|slide|fade"} ],
  "subs":     [ {"s0": src, "s1": src, "text": "...", "hl": ["关键词"]} ],
  "sfx":      [ {"t": out_sec | "src_t": src, "kind": "whoosh|click|pop|hit|ding|riser", "db": 0} ],
  "music":    {"bpm": 120, "rel_db": -17, "duck_db": 7}
}
"""
import json, os, subprocess, sys, tempfile, wave
import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfx, audio  # noqa: E402

W, H = gfx.W, gfx.H
PIP_C = (853, 395)
PIP_D = 270


def run(cmd):
    subprocess.run(cmd, check=True)


# ------------------------------------------------------------------ timeline
class Timeline:
    def __init__(self, edl):
        self.fps = edl.get("fps", 30)
        self.shots = edl["shots"]
        f = 0
        for s in self.shots:
            s["nf"] = max(1, round((s["out"] - s["in"]) * self.fps))
            s["f0"] = f
            f += s["nf"]
        self.nframes = f
        self.duration = f / self.fps

    def src2out(self, t, prefer_end=False):
        for s in self.shots:
            if s["in"] - 1e-3 <= t <= s["out"] + 1e-3:
                return s["f0"] / self.fps + (t - s["in"])
        # not inside a shot: snap to the next shot start (or previous end)
        best = None
        for s in self.shots:
            if prefer_end and s["out"] <= t:
                best = (s["f0"] + s["nf"]) / self.fps
            if not prefer_end and s["in"] >= t:
                return s["f0"] / self.fps
        return best if best is not None else self.duration


# ------------------------------------------------------------------ graphics
def ease_out_back(x, k=1.6):
    x = x - 1
    return 1 + (k + 1) * x ** 3 + k * x ** 2


def build_layers(edl, tl):
    out = []
    for g in edl.get("graphics", []):
        t0 = g["t0"] if "t0" in g else tl.src2out(g["src_t0"])
        t1 = g.get("t1")
        if t1 is None:
            t1 = tl.src2out(g["src_t1"], prefer_end=True)
        if t1 == "end":
            t1 = tl.duration
        a = g.get("args", {})
        typ = g["type"]
        anim = g.get("anim", {"intro": "pop", "tag": "slide"}.get(typ, "pop"))
        if typ == "intro":
            out.append((t0, t1, gfx.intro_card(**a), anim))
        elif typ == "tag":
            out.append((t0, t1, gfx.topic_tag(**a), anim))
        elif typ == "gold_card":
            out.append((t0, t1, gfx.gold_card(**a), anim))
        elif typ == "metal_word":
            out.append((t0, t1, gfx.metal_word(**a), anim))
        elif typ == "flow":
            tk = g.get("t_kids") if "t_kids" in g else tl.src2out(g["src_t_kids"])
            top, kids = gfx.flow_parts(**a)
            out.append((t0, t1, top, anim))
            out.append((tk, t1, kids, "pop"))
        else:
            raise ValueError(typ)
    return out


def build_subs(edl, tl):
    subs = []
    for s in edl.get("subs", []):
        t0 = s["t0"] if "t0" in s else tl.src2out(s["s0"])
        t1 = s["t1"] if "t1" in s else tl.src2out(s["s1"], prefer_end=True)
        if t1 - t0 < 0.05:
            continue
        subs.append((t0, t1, gfx.subtitle(s["text"], s.get("hl", []))))
    return subs


def blend(frame, rgba, x, y, amul=1.0):
    h, w = rgba.shape[:2]
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    src = rgba[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32)
    a = src[..., 3:4] / 255.0 * amul
    region = frame[y0:y1, x0:x1]
    region *= (1 - a)
    region += src[..., :3] * a


def draw_layer(frame, layer, t, t0, t1, anim):
    dt_in = t - t0
    dt_out = t1 - t
    amul = 1.0
    rgba, x, y = layer.rgba, layer.x, layer.y
    IN = 0.18
    if dt_in < IN:
        p = max(dt_in / IN, 0)
        if anim == "pop":
            s = 0.86 + 0.14 * ease_out_back(p)
            amul = min(1, p * 1.6)
            if abs(s - 1) > 1e-3:
                pm = rgba.astype(np.float32)
                pm[..., :3] *= pm[..., 3:4] / 255
                nw, nh = max(1, int(layer.w * s)), max(1, int(layer.h * s))
                pm = cv2.resize(pm, (nw, nh), interpolation=cv2.INTER_LINEAR)
                a = np.clip(pm[..., 3:4], 1e-3, 255)
                pm[..., :3] = np.where(pm[..., 3:4] > 0.5, pm[..., :3] * 255 / a, 0)
                rgba = np.clip(pm, 0, 255).astype(np.uint8)
                x = int(layer.x + (layer.w - nw) / 2)
                y = int(layer.y + (layer.h - nh) / 2)
        elif anim == "slide":
            x = int(layer.x - (1 - (1 - (1 - p) ** 3)) * (layer.w + 40))
        else:
            amul = p
    if dt_out < 0.12:
        amul *= max(dt_out / 0.12, 0)
    blend(frame, rgba, x, y, amul)


# ------------------------------------------------------------------ video
class ShotReader:
    """Decodes one shot's frames (fit-to-fill 1080x1920) from `src` starting at `start`."""
    def __init__(self, src, start, nf, fps):
        dur = nf / fps + 0.2
        self.p = subprocess.Popen(
            ["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-i", src, "-t", f"{dur:.3f}",
             "-vf", f"fps={fps},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
             "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
            stdout=subprocess.PIPE)
        self.last = None

    def read(self):
        buf = self.p.stdout.read(W * H * 3)
        if len(buf) == W * H * 3:
            self.last = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        return self.last

    def close(self):
        self.p.stdout.close()
        self.p.kill()
        self.p.wait()


def view_crop(img, view, p):
    if not view:
        return img
    z = view.get("z0", 1.0) + (view.get("z1", view.get("z0", 1.0)) - view.get("z0", 1.0)) * p
    if z <= 1.0001:
        return img
    cw, ch = W / z, H / z
    cx = min(max(view.get("cx", W / 2), cw / 2), W - cw / 2)
    cy = min(max(view.get("cy", H / 2), ch / 2), H - ch / 2)
    M = np.float32([[z, 0, -(cx - cw / 2) * z], [0, z, -(cy - ch / 2) * z]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def pip_patch(img, pip):
    s = pip.get("size", 420)
    x0 = int(min(max(pip["cx"] - s / 2, 0), W - s))
    y0 = int(min(max(pip["cy"] - s / 2, 0), H - s))
    sq = cv2.resize(img[y0:y0 + s, x0:x0 + s], (PIP_D, PIP_D), interpolation=cv2.INTER_AREA)
    return sq


def render_video(edl, tl, out_path, audio_path, stills=None, preview=False):
    src = edl["source"]
    plate_mul = (0.40 * gfx.vignette() * (1 - gfx.halftone()))[..., None].astype(np.float32)
    # B-roll grade (reference look): partly desaturated, dimmed, dot screen + vignette
    broll_mul = (0.78 * gfx.vignette(strength=0.45) * (1 - gfx.halftone(alpha=0.22)))[..., None].astype(np.float32)
    layers = build_layers(edl, tl)
    subs = build_subs(edl, tl)
    ring = np.array(gfx.pip_ring(PIP_D))
    yy, xx = np.mgrid[0:PIP_D, 0:PIP_D]
    circ = (((xx - PIP_D / 2 + 0.5) ** 2 + (yy - PIP_D / 2 + 0.5) ** 2) <= (PIP_D / 2 - 1) ** 2).astype(np.float32)
    circ = cv2.GaussianBlur(circ, (3, 3), 0)[..., None]
    stills = sorted(stills or [])
    enc = None
    if not stills:
        enc = subprocess.Popen(
            ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(tl.fps), "-i", "-", "-i", audio_path, "-map", "0:v", "-map", "1:a",
             "-c:v", "libx264", "-preset", "veryfast" if preview else "medium", "-crf", "20" if preview else "17",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
             out_path], stdin=subprocess.PIPE)
    saved = []
    for si, shot in enumerate(tl.shots):
        f0, nf = shot["f0"], shot["nf"]
        if stills and not any(f0 <= int(round(t * tl.fps)) < f0 + nf for t in stills):
            continue
        br = shot.get("broll")
        rd = ShotReader(src, shot["in"], nf, tl.fps)
        bd = ShotReader(br["file"], br.get("start", 0), nf, tl.fps) if br else None
        for k in range(nf):
            raw = rd.read()
            main = bd.read() if bd else raw
            fi = f0 + k
            t = fi / tl.fps
            if stills and not any(int(round(s * tl.fps)) == fi for s in stills):
                continue
            img = view_crop(main, shot.get("view"), k / max(nf - 1, 1))
            fr = img.astype(np.float32)
            grade = shot.get("grade") or ("plate" if shot.get("plate") else ("broll" if br else None))
            if grade in ("plate", "broll"):
                lum = fr.mean(axis=2, keepdims=True)
                fr = fr * 0.6 + lum * 0.4  # desaturate 40%
                fr *= plate_mul if grade == "plate" else broll_mul
            # transitions into this shot
            tr = shot.get("trans", "cut")
            if tr == "whip" and k < 5:
                L = int(90 * (1 - k / 5)) | 1
                kern = np.zeros((1, L), np.float32); kern[0, :] = 1 / L
                fr = cv2.filter2D(fr, -1, kern)
                fr = np.roll(fr, int(60 * (1 - k / 5)), axis=1)
            if shot.get("pip"):
                patch = pip_patch(raw, shot["pip"]).astype(np.float32)
                x0, y0 = PIP_C[0] - PIP_D // 2, PIP_C[1] - PIP_D // 2
                reg = fr[y0:y0 + PIP_D, x0:x0 + PIP_D]
                reg *= (1 - circ); reg += patch * circ
                blend(fr, ring, PIP_C[0] - ring.shape[1] // 2, PIP_C[1] - ring.shape[0] // 2)
            for (t0, t1, L, anim) in layers:
                if t0 <= t < t1:
                    draw_layer(fr, L, t, t0, t1, anim)
            for (t0, t1, L) in subs:
                if t0 <= t < t1:
                    blend(fr, L.rgba, L.x, L.y)
            if tr == "flash" and k < 6:
                a = 0.85 * (1 - k / 6)
                fr = fr * (1 - a) + 255 * a
            out = np.clip(fr, 0, 255).astype(np.uint8)
            if stills:
                p = os.path.splitext(out_path)[0] + f"_still_{t:06.2f}.jpg"
                Image.fromarray(out).save(p, quality=90); saved.append(p)
            else:
                enc.stdin.write(out.tobytes())
        rd.close()
        if bd:
            bd.close()
        if not stills:
            print(f"shot {si + 1}/{len(tl.shots)}", file=sys.stderr, flush=True)
    if enc:
        enc.stdin.close(); enc.wait()
    return saved


# ------------------------------------------------------------------ audio
def read_wav(p):
    with wave.open(p) as w:
        n, ch = w.getnframes(), w.getnchannels()
        a = np.frombuffer(w.readframes(n), np.int16).astype(np.float32) / 32768
    return a.reshape(-1, ch)


def write_wav(p, x):
    x = np.clip(x, -1, 1)
    with wave.open(p, "wb") as w:
        w.setnchannels(x.shape[1] if x.ndim > 1 else 1); w.setsampwidth(2); w.setframerate(audio.SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def render_audio(edl, tl, tmp):
    SR = audio.SR
    raw = os.path.join(tmp, "src48k.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", edl["source"], "-vn", "-ac", "2", "-ar", str(SR), raw])
    a = read_wav(raw).mean(1)
    parts = []
    fade = int(0.008 * SR)
    for s in tl.shots:
        i0 = int(s["in"] * SR)
        n = int(round(s["nf"] / tl.fps * SR))
        seg = a[i0:i0 + n].copy()
        if len(seg) < n:
            seg = np.pad(seg, (0, n - len(seg)))
        if s.get("mute"):
            seg[:] = 0
        seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
        parts.append(seg)
    v = np.concatenate(parts)
    vin = os.path.join(tmp, "voice_in.wav"); vout = os.path.join(tmp, "voice_out.wav")
    write_wav(vin, v[:, None])
    run(["ffmpeg", "-v", "error", "-y", "-i", vin, "-af",
         "highpass=f=85,afftdn=nf=-28,acompressor=threshold=-24dB:ratio=3:attack=5:release=150:makeup=4,"
         "equalizer=f=3500:t=q:w=1:g=2", vout])
    v = read_wav(vout)[:, 0]
    events = []
    for e in edl.get("sfx", []):
        t = e["t"] if "t" in e else tl.src2out(e["src_t"])
        events.append((t, e["kind"], e.get("db", 0)))
    m = edl.get("music", {})
    mixd = audio.mix(v, tl.duration, events, music_rel_db=m.get("rel_db", -17),
                     duck_db=m.get("duck_db", 7), bpm=m.get("bpm", 120))
    pre = os.path.join(tmp, "mix_pre.wav"); fin = os.path.join(tmp, "mix.wav")
    write_wav(pre, mixd * 0.5)
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", pre, "-af",
                           "loudnorm=I=-14:TP=-2.0:LRA=11:print_format=json", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    js = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
    run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af",
         f"loudnorm=I=-14:TP=-2.0:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
         f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true",
         "-ar", str(SR), fin])
    return fin


def main():
    args = sys.argv[1:]
    edl = json.load(open(args[0]))
    out = args[1]
    preview = "--preview" in args
    stills = None
    if "--stills" in args:
        stills = [float(x) for x in args[args.index("--stills") + 1].split(",")]
    tl = Timeline(edl)
    print(f"duration {tl.duration:.2f}s, {tl.nframes} frames, {len(tl.shots)} shots", file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmp:
        ap = None if stills else render_audio(edl, tl, tmp)
        saved = render_video(edl, tl, out, ap, stills, preview)
    for p in saved:
        print(p)


if __name__ == "__main__":
    main()
