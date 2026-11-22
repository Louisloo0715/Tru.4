#!/usr/bin/env python3
"""Synthesize a royalty-free dark-ambient horror bed (for when no generated/stock track is available).

usage: python3 -I synth_bgm.py out.wav [--secs 180] [--seed 7]
Sections (same layout as assets/music/horror_bgm so music_at habits carry over):
  0-70s   unease: low pad (A minor), sparse detuned piano notes with long echo
  70-118s tension: + slow sub pulse (heartbeat-like), ticking clock, pad rises a semitone cluster
  118-end dread: + high string cluster swells, dissonant piano, louder pulse
"""
import sys, os
import numpy as np
from scipy.signal import fftconvolve
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import audio, render  # noqa: E402

SR = 48000


def env_ar(n, a, r):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-np.maximum(0, t - a) / r)


def main():
    out = sys.argv[1]
    secs = int(sys.argv[sys.argv.index("--secs") + 1]) if "--secs" in sys.argv else 180
    rng = np.random.default_rng(int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 7)
    n = secs * SR; t = np.arange(n) / SR; y = np.zeros(n)
    sec = lambda a, b: np.clip((t - a) / 4, 0, 1) * np.clip((b - t) / 4 + 1, 0, 1)
    # pad: A minor -> F -> D minor -> E, 10 s per chord, detuned sines through a slow filter sweep
    chords = [[110, 130.81, 164.81], [87.31, 110, 130.81], [73.42, 87.31, 110], [82.41, 103.83, 123.47]]
    pad = np.zeros(n)
    for i, ch in enumerate(chords * (secs // 40 + 1)):
        a, b = i * 10.0, i * 10.0 + 12.0
        if a >= secs: break
        m = (t >= a) & (t < b); tt = t[m] - a
        g = np.minimum(1, tt / 3) * np.minimum(1, (12 - tt) / 3)
        for f in ch:
            for d in (-0.6, 0, 0.7):
                pad[m] += np.sin(2 * np.pi * (f + d) * tt + rng.random() * 6) * g
                pad[m] += 0.25 * np.sin(2 * np.pi * 2 * (f + d) * tt) * g
    pad = audio.lp(pad, 900) * (0.55 + 0.25 * np.sin(2 * np.pi * t / 37))
    y += pad * 0.08
    # cluster rise in tension / dread
    for f in (220, 233.08, 246.94):
        y += np.sin(2 * np.pi * f * t + rng.random() * 6) * 0.018 * (sec(70, secs) * 0.6 + sec(118, secs) * 0.8)
    # piano-ish notes
    scale = [220, 261.63, 293.66, 329.63, 349.23, 440, 523.25, 311.13]
    tp = 3.0
    while tp < secs - 3:
        f = scale[rng.integers(0, 6 if tp < 118 else 8)]
        L = int(4 * SR); i0 = int(tp * SR); tt = np.arange(L) / SR
        note = sum(np.sin(2 * np.pi * f * k * tt * (1 + 0.0007 * k)) / k ** 1.5 for k in (1, 2, 3, 4)) * np.exp(-tt * 1.4)
        y[i0:i0 + L] += note[:n - i0] * 0.05
        tp += rng.uniform(2.5, 5.0) if tp < 70 else rng.uniform(1.6, 3.2)
    # sub pulse (double beat) from 70 s
    pulse = np.zeros(n)
    for b in np.arange(70, secs, 1.0):
        for off, amp in ((0, 1.0), (0.28, 0.6)):
            i0 = int((b + off) * SR); L = int(0.4 * SR); tt = np.arange(L) / SR
            pulse[i0:i0 + L] += (np.sin(2 * np.pi * 48 * tt) * np.exp(-tt * 9) * amp)[:max(0, n - i0)]
    y += pulse * 0.22 * (sec(70, secs) * 0.6 + sec(118, secs) * 0.5)
    # clock tick 70-118
    for b in np.arange(70, min(118, secs), 0.5):
        i0 = int(b * SR); L = int(0.03 * SR)
        y[i0:i0 + L] += audio.hp(rng.standard_normal(L), 3000) * np.exp(-np.arange(L) / SR * 200) * 0.05
    # high string swells in dread
    sw = np.zeros(n)
    for f in (880, 932.33, 987.77):
        sw += np.sin(2 * np.pi * f * t + 0.003 * np.sin(2 * np.pi * 5 * t)) / 3
    y += sw * 0.03 * sec(118, secs) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 9) ** 2)
    # reverb
    L = int(3.5 * SR); ir = rng.standard_normal(L) * np.exp(-np.arange(L) / SR * 2.0); ir = audio.lp(ir, 4000)
    wet = fftconvolve(y, ir)[:n]; wet *= np.sqrt(np.mean(y ** 2)) / (np.sqrt(np.mean(wet ** 2)) + 1e-9)
    y = 0.6 * y + 0.55 * wet
    y = y / (np.abs(y).max() + 1e-9) * 0.8
    y[-2 * SR:] *= np.linspace(1, 0, 2 * SR)
    render.write_wav(out, y[:, None])
    print("wrote", out, secs, "s")


if __name__ == "__main__":
    main()
