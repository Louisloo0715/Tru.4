"""2D mascot lip-sync for Mandarin: word timestamps + pinyin finals + loudness gate -> mouth sprite per frame.

Mouth set (any subset works, missing ones fall back):
  closed  - idle / b p m onsets / silence
  half    - e, i, ei, en, eng, ie, in, ing, -i (zhi chi shi ri zi ci si), quick unstressed syllables
  open    - generic open
  wide    - a, ia, ua, ai, ao, an, ang, ian, iang, uan, uang
  o       - o, uo, ou, u, ong, iong, iu, ü, un
"""
import random
import numpy as np
from pypinyin import pinyin, Style

WIDE = ("a", "ai", "ao", "an", "ang", "ia", "ua", "iao", "ian", "iang", "uai", "uan", "uang", "van")
ROUND = ("o", "uo", "ou", "u", "ong", "iong", "iu", "v", "ve", "vn", "un", "ue", "iou", "uei", "ui")
LABIAL = ("b", "p", "m", "f")


def char_shape(ch):
    if not ("一" <= ch <= "鿿"):
        return ("open", False) if ch.isalpha() else None
    fin = pinyin(ch, style=Style.FINALS, strict=False)[0][0]
    ini = pinyin(ch, style=Style.INITIALS, strict=False)[0][0]
    if fin in WIDE:
        shape = "wide"
    elif fin in ROUND:
        shape = "o"
    else:
        shape = "half"
    return shape, ini in LABIAL


def char_spans(words):
    """words: [{'s','e','w'}] -> per-character (t0, t1, char), splitting multi-char words evenly."""
    out = []
    for w in words:
        txt = [c for c in w["w"].strip() if c.strip() and c not in "，。、？！,.?!：:；;"]
        if not txt:
            continue
        dur = max(w["e"] - w["s"], 0.06)
        step = dur / len(txt)
        for i, c in enumerate(txt):
            out.append((w["s"] + i * step, w["s"] + (i + 1) * step, c))
    return out


def mouth_track(words, n_frames, fps, rms_db=None, gate_db=-42, offset=0.0, seed=1):
    """Return list of mouth names per output frame. `offset` maps word time -> output time."""
    track = ["closed"] * n_frames
    spans = char_spans(words)
    alt = 0
    for (t0, t1, c) in spans:
        r = char_shape(c)
        if r is None:
            continue
        shape, labial = r
        if shape == "open":
            shape = "open"
        a = int(round((t0 + offset) * fps)); b = int(round((t1 + offset) * fps))
        b = max(b, a + 2)
        n = b - a
        seq = []
        if labial and n >= 3:
            seq.append("closed")
        peak = shape
        if shape == "wide" and n <= 3:  # short syllables don't reach the full open
            peak = "open"
        if shape == "half" and alt % 3 == 2:
            peak = "open"  # a little variety
        alt += 1
        rest = n - len(seq)
        k_peak = max(1, int(round(rest * 0.65)))
        seq += [peak] * k_peak + ["half" if peak != "half" else "closed"] * (rest - k_peak)
        for i, s in enumerate(seq):
            if 0 <= a + i < n_frames:
                track[a + i] = s
    if rms_db is not None:  # silence gate
        for i in range(n_frames):
            if rms_db[min(i, len(rms_db) - 1)] < gate_db:
                track[i] = "closed"
    # de-flicker: no single-frame states
    for i in range(1, n_frames - 1):
        if track[i] != track[i - 1] and track[i] != track[i + 1]:
            track[i] = track[i - 1]
    return track


def blink_track(n_frames, fps, seed=3, every=(2.2, 5.0), length=4):
    rng = random.Random(seed)
    out = [False] * n_frames
    t = rng.uniform(0.8, 2.0)
    while t * fps < n_frames:
        f = int(t * fps)
        for i in range(f, min(n_frames, f + length)):
            out[i] = True
        t += rng.uniform(*every)
    return out


def frame_rms_db(mono, sr, fps):
    hop = sr / fps
    n = int(len(mono) / hop)
    out = np.empty(n)
    for i in range(n):
        seg = mono[int(i * hop):int((i + 1) * hop)]
        out[i] = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)
    return out
