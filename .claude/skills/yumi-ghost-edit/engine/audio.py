"""Audio for the explainer style: procedural royalty-free BGM, SFX kit, ducking mix.

All functions work on float32 mono/stereo numpy arrays at SR=48000.
"""
import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
rng = np.random.default_rng(7)


def db(x):
    return 10 ** (x / 20)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def env(n, a, d, s=0.0, r=0.0, sus_len=0):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    e = np.concatenate([np.linspace(0, 1, max(a, 1)), np.linspace(1, s, max(d, 1)),
                        np.full(sus_len, s), np.linspace(s, 0, max(r, 1))])
    out = np.zeros(n, np.float32)
    out[:min(n, len(e))] = e[:n]
    return out


def saw(freq, n, detune=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for d in (-detune, 0, detune):
        ph = (t * freq * (1 + d)) % 1.0
        out += 2 * ph - 1
    return out / 3


# ------------------------------------------------------------------ music
def note(n):  # midi -> Hz
    return 440 * 2 ** ((n - 69) / 12)


def music(duration, bpm=120, seed=3):
    """Driving 4-on-the-floor electronic bed: kick, offbeat hats, sidechained pad, pluck bass.
    Am - F - C - G, one chord per bar."""
    beat = 60 / bpm
    bar = beat * 4
    n = int((duration + bar) * SR)
    out = np.zeros(n)
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    roots = [45, 41, 48, 43]
    nb = int(np.ceil(duration / beat)) + 4
    kick_n = int(0.35 * SR)
    t = np.arange(kick_n) / SR
    kick = np.sin(2 * np.pi * (45 * t + 60 * (1 - np.exp(-t * 30)) / 30)) * np.exp(-t * 9)
    hat_n = int(0.06 * SR)
    hat = hp(rng.standard_normal(hat_n), 7000) * np.exp(-np.arange(hat_n) / SR * 60)
    clap_n = int(0.18 * SR)
    clap = bp(rng.standard_normal(clap_n), 900, 3000) * np.exp(-np.arange(clap_n) / SR * 22)
    pump = np.ones(n)
    for b in range(nb):
        s = int(b * beat * SR)
        if s >= n:
            break
        e = min(n, s + kick_n)
        out[s:e] += 0.9 * kick[:e - s]
        pe = min(n, s + int(beat * SR))
        pump[s:pe] = 0.35 + 0.65 * np.clip(np.arange(pe - s) / (0.22 * SR), 0, 1)
        hs = s + int(beat / 2 * SR)
        if hs + hat_n < n:
            out[hs:hs + hat_n] += 0.22 * hat
        if b % 2 == 1 and s + clap_n < n:
            out[s:s + clap_n] += 0.18 * clap
    # pad + bass per bar
    nbar = int(np.ceil(duration / bar)) + 1
    pad = np.zeros(n)
    bass = np.zeros(n)
    for i in range(nbar):
        s = int(i * bar * SR)
        L = int(bar * SR)
        if s >= n:
            break
        L = min(L, n - s)
        ch = chords[i % 4]
        p = sum(saw(note(m), L, 0.004) for m in ch) / 3
        pad[s:s + L] += p * env(L, 0.08, 0.3, 0.7, 0.2, max(0, L - int(0.6 * SR)))
        for k in range(8):  # 8th-note pluck bass
            bs = s + int(k * beat / 2 * SR)
            bl = int(beat / 2 * SR * 0.9)
            if bs + bl > n:
                break
            bass[bs:bs + bl] += saw(note(roots[i % 4] - 12 + (12 if k % 4 == 3 else 0)), bl) * env(bl, 0.005, 0.18, 0.2, 0.05)
    pad = lp(pad, 2200) * 0.30 * pump
    bass = lp(bass, 700) * 0.42 * pump
    out = out + pad + bass
    out = out[:int(duration * SR)]
    fade = int(0.8 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    out[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))
    stereo = np.stack([out, np.roll(out, 240) * 0.98], 1)  # tiny width
    return (stereo / (np.max(np.abs(stereo)) + 1e-9) * 0.7).astype(np.float32)


# ------------------------------------------------------------------ sfx kit
def sfx(kind):
    if kind == "whoosh":
        L = int(0.42 * SR)
        x = rng.standard_normal(L)
        t = np.linspace(0, 1, L)
        lo, mid, hi = bp(x, 250, 1200), bp(x, 1200, 4000), bp(x, 4000, 10000)
        w = np.sin(np.pi * t)
        out = lo * (1 - t) + mid * w + hi * t ** 2
        return out * np.sin(np.pi * t) ** 1.5 * 0.6
    if kind == "click":
        L = int(0.05 * SR)
        t = np.arange(L) / SR
        return (np.sin(2 * np.pi * 2400 * t) * 0.6 + hp(rng.standard_normal(L), 4000) * 0.3) * np.exp(-t * 120)
    if kind == "pop":
        L = int(0.12 * SR)
        t = np.arange(L) / SR
        f = 900 * np.exp(-t * 18) + 300
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35) * 0.8
    if kind == "hit":
        L = int(1.0 * SR)
        t = np.arange(L) / SR
        sub = np.sin(2 * np.pi * (48 * t + 80 * (1 - np.exp(-t * 20)) / 20)) * np.exp(-t * 3.5)
        n = lp(rng.standard_normal(L), 1800) * np.exp(-t * 14) * 0.5
        return (sub + n) * 0.9
    if kind == "ding":
        L = int(0.9 * SR)
        t = np.arange(L) / SR
        return (np.sin(2 * np.pi * 1568 * t) + 0.5 * np.sin(2 * np.pi * 2349 * t)) * np.exp(-t * 5) * 0.35
    if kind == "riser":
        L = int(1.2 * SR)
        t = np.linspace(0, 1, L)
        x = hp(rng.standard_normal(L), 2000) * t ** 2
        return x * 0.4
    raise ValueError(kind)


# ------------------------------------------------------------------ mix
def rms_env(x, win=0.05):
    w = max(1, int(win * SR)); c = np.cumsum(np.concatenate([[0.0], np.asarray(x, np.float64) ** 2]))
    n = len(x); i = np.arange(n); lo = np.clip(i - w // 2, 0, n); hi = np.clip(i - w // 2 + w, 0, n)
    return np.sqrt((c[hi] - c[lo]) / np.maximum(hi - lo, 1) + 1e-12)


def duck_gain(voice_mono, depth_db=7, attack=0.03, release=0.35, thresh_db=-38):
    e = rms_env(voice_mono)
    step = SR // 1000  # smooth at 1 kHz control rate
    active = (20 * np.log10(e[::step]) > thresh_db).astype(np.float64)
    g = np.empty_like(active)
    a = np.exp(-1 / (attack * 1000)); r = np.exp(-1 / (release * 1000))
    y = 0.0
    for i, v in enumerate(active):
        c = a if v > y else r
        y = c * y + (1 - c) * v
        g[i] = y
    g = np.interp(np.arange(len(voice_mono)) / step, np.arange(len(g)), g)
    return db(-depth_db * g)


def mix(voice, duration, events, music_rel_db=-17, duck_db=7, sfx_rel_db=-9, bpm=120):
    """voice: mono float array at SR. events: [(t, kind, gain_db)].
    Music sits music_rel_db below the voice's speech RMS and ducks a further duck_db
    under speech (so ~-24 dB under voice while talking, swells in pauses)."""
    n = int(duration * SR)
    v = np.zeros(n); v[:min(n, len(voice))] = voice[:n]
    e = rms_env(v)
    speech_rms = np.median(e[20 * np.log10(e) > -38]) if np.any(20 * np.log10(e) > -38) else 0.05
    m = music(duration, bpm)
    m_rms = np.sqrt(np.mean(m ** 2))
    m = m * (speech_rms * db(music_rel_db) / m_rms)
    g = duck_gain(v, duck_db)
    m = m * g[:, None]
    out = np.stack([v, v], 1) + m
    for t, kind, gdb in events:
        s = sfx(kind)
        s = s / (np.sqrt(np.mean(s ** 2)) + 1e-9) * speech_rms * db(sfx_rel_db + gdb)
        i = int(t * SR)
        if i >= n:
            continue
        L = min(len(s), n - i)
        out[i:i + L] += s[:L, None]
    return out.astype(np.float32)
