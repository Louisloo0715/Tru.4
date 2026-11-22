#!/usr/bin/env python3
"""Synthesize a royalty-free eerie horror bed (when no generated/stock track is available).

usage: python3 -I synth_bgm.py out.wav [--secs 180] [--seed 7]

Lesson from episode 2: a pad that lives below 200 Hz is inaudible on phones/laptops ("BGM 沒聽到"), even when its RMS
is only 12 dB under the voice. Everything here sits in 300 Hz - 4 kHz so it reads on small speakers.
Sections (same layout as assets/music/horror_bgm, so music_at habits carry over):
  0-70s    unease : warm-ish mid pad, slow out-of-tune music box motif, faint high cluster
  70-118s  tension: + tremolo strings, ticking, reversed swells every ~8 s, motif detunes
  118-end  dread  : + dissonant high strings, whisper texture, low booms, motif in a lower, slower, wobbling voice
"""
import sys, os
import numpy as np
from scipy.signal import fftconvolve
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import audio, render  # noqa: E402

SR = 48000


def main():
    out = sys.argv[1]
    secs = int(sys.argv[sys.argv.index("--secs") + 1]) if "--secs" in sys.argv else 180
    rng = np.random.default_rng(int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 7)
    n = secs * SR; t = np.arange(n) / SR; y = np.zeros(n)
    ramp = lambda a: np.clip((t - a) / 5, 0, 1)
    tens, dread = ramp(70), ramp(118)

    # 1) mid pad: A minor / F / D minor / E, voiced in 220-660 Hz, saw-ish (odd+even harmonics), slow filter breathing
    chords = [[220, 261.63, 329.63], [174.61, 220, 261.63], [146.83, 174.61, 220], [164.81, 207.65, 246.94]]
    pad = np.zeros(n)
    for i in range(int(secs / 10) + 1):
        ch = chords[i % 4]; a = i * 10.0
        m = (t >= a) & (t < a + 12); tt = t[m] - a
        g = np.minimum(1, tt / 3) * np.minimum(1, (12 - tt) / 3)
        for f in ch:
            for d in (-0.8, 0.0, 0.9):
                for k, amp in ((1, 1), (2, 0.45), (3, 0.25), (4, 0.12)):
                    pad[m] += amp * np.sin(2 * np.pi * k * (f + d) * tt + rng.random() * 6) * g
    pad = audio.bp(pad, 250, 2500) * (0.7 + 0.3 * np.sin(2 * np.pi * t / 23))
    y += pad / (np.abs(pad).max() + 1e-9) * 0.30

    # 2) music box motif (A minor), out of tune; in dread it drops an octave, slows and wobbles
    motif = [659.25, 523.25, 440.0, 493.88, 659.25, 587.33, 523.25, 493.88, 440.0, 415.30, 440.0, 0]
    tp, idx = 2.0, 0
    while tp < secs - 2:
        f = motif[idx % len(motif)]; idx += 1
        step = 0.55 if tp < 118 else 0.8
        if f:
            if tp >= 118: f /= 2
            f *= 1 + rng.normal(0, 0.004) + (0.012 * np.sin(tp) if tp >= 70 else 0)
            L = int(2.2 * SR); i0 = int(tp * SR); tt = np.arange(L) / SR
            wob = 1 + (0.01 * np.sin(2 * np.pi * 5.5 * tt) if tp >= 118 else 0)
            ph = 2 * np.pi * f * np.cumsum(np.full(L, 1.0) * wob) / SR
            note = (np.sin(ph) + 0.35 * np.sin(3 * ph) + 0.15 * np.sin(5.04 * ph)) * np.exp(-tt * 2.2)
            lvl = 0.16 if tp < 70 else 0.13
            y[i0:i0 + L] += note[:max(0, n - i0)] * lvl
        tp += step
        if idx % len(motif) == 0:
            tp += 2.5 if tp < 70 else 1.2

    # 3) high cluster (faint from the start, grows) + tremolo strings in tension/dread
    cl = sum(np.sin(2 * np.pi * f * t + rng.random() * 6) for f in (880, 932.33, 1046.5)) / 3
    y += cl * (0.02 + 0.05 * tens + 0.06 * dread) * (0.6 + 0.4 * np.sin(2 * np.pi * t / 11) ** 2)
    trem = (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 7 * t))) * 0.8 + 0.2
    st = sum(np.sin(2 * np.pi * f * t + 0.004 * np.sin(2 * np.pi * 5 * t)) for f in (622.25, 659.25, 698.46)) / 3
    y += audio.lp(st * trem, 3000) * 0.07 * (tens * (1 - dread) + 1.4 * dread)

    # 4) ticking clock (tension)
    for b in np.arange(70, min(118, secs), 0.5):
        i0 = int(b * SR); L = int(0.03 * SR)
        y[i0:i0 + L] += audio.bp(rng.standard_normal(L), 2000, 6000) * np.exp(-np.arange(L) / SR * 180) * 0.12

    # 5) reversed swells every ~8 s from 70 s; low booms at section starts and every 16 s in dread
    for b in np.arange(76, secs - 3, 8.0):
        L = int(2.0 * SR); tt = np.arange(L) / SR
        sw = audio.bp(rng.standard_normal(L), 400, 3000) * np.exp(-tt * 2.5)
        sw = fftconvolve(sw, rng.standard_normal(int(0.6 * SR)) * np.exp(-np.arange(int(0.6 * SR)) / SR * 6))[:L][::-1]
        i1 = int(b * SR); i0 = i1 - L
        if i0 > 0:
            y[i0:i1] += sw / (np.abs(sw).max() + 1e-9) * 0.22
    for b in [70.0, 118.0] + list(np.arange(134, secs - 2, 16.0)):
        L = int(2.5 * SR); tt = np.arange(L) / SR; i0 = int(b * SR)
        boom = np.sin(2 * np.pi * (55 + 30 * np.exp(-tt * 8)) * tt) * np.exp(-tt * 2.2)
        boom += audio.bp(rng.standard_normal(L), 200, 1200) * np.exp(-tt * 9) * 0.4  # audible attack on small speakers
        y[i0:i0 + L] += boom[:max(0, n - i0)] * 0.35

    # 6) whisper texture in dread: formant-filtered noise phrases
    for b in np.arange(121, secs - 3, 5.5):
        L = int(rng.uniform(0.8, 1.6) * SR); tt = np.arange(L) / SR; i0 = int(b * SR)
        x = audio.bp(rng.standard_normal(L), 1200, 4500) * (0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(4, 7) * tt)) ** 2
        x *= np.sin(np.pi * tt / tt[-1])
        y[i0:i0 + L] += x[:max(0, n - i0)] * 0.10

    # reverb + normalize
    L = int(3.0 * SR); ir = rng.standard_normal(L) * np.exp(-np.arange(L) / SR * 2.3); ir = audio.lp(ir, 5000)
    wet = fftconvolve(y, ir)[:n]; wet *= np.sqrt(np.mean(y ** 2)) / (np.sqrt(np.mean(wet ** 2)) + 1e-9)
    y = 0.65 * y + 0.5 * wet
    y = audio.hp(y, 120)
    y = y / (np.abs(y).max() + 1e-9) * 0.85
    y[-2 * SR:] *= np.linspace(1, 0, 2 * SR)
    render.write_wav(out, y[:, None])
    print("wrote", out, secs, "s")


if __name__ == "__main__":
    main()
