#!/usr/bin/env python3
"""Snap every narration piece to real silence so no word is clipped (user: "有些還沒說完就砍掉的要補回來").

usage: python3 -I snap_edges.py edl_in.json edl_out.json [--report]
For each block src range [a, b]:
  * end b  -> moved forward until the voice stays below -38 dB for 120 ms (at most +0.7 s), never into the next
             kept range of the same block;
  * start a -> moved back to where the sound begins (at most -0.3 s), never into the previous kept range.
Ranges that become adjacent/overlapping are merged. Run it before subtitles (times shift a little).
"""
import json, sys, wave
import numpy as np

SR = 48000; THR = -38.0; HOLD = 0.12; STEP = 0.01


def main():
    src, dst = sys.argv[1], sys.argv[2]
    e = json.load(open(src))
    w = wave.open(e["audio"]); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    if w.getnchannels() > 1:
        v = v.reshape(-1, w.getnchannels()).mean(1)

    def loud(t):
        s = v[max(0, int(t * SR)):int((t + 0.02) * SR)]
        return len(s) and 20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-9) > THR

    def quiet_run(t):
        return not any(loud(t + k * STEP) for k in range(int(HOLD / STEP)))

    moved = []
    for bi, bl in enumerate(e["blocks"]):
        if "src" not in bl:
            continue
        rs = sorted(bl["src"])
        out = []
        for i, (a, b) in enumerate(rs):
            lo = out[-1][1] if out else a - 0.3
            hi = rs[i + 1][0] if i + 1 < len(rs) else b + 0.7
            a2 = a
            while a2 - STEP > max(lo, a - 0.3) and loud(a2 - STEP):
                a2 -= STEP
            b2 = b
            while b2 + STEP < min(hi, b + 0.7) and not quiet_run(b2):
                b2 += STEP
            a2, b2 = round(a2, 2), round(b2, 2)
            if abs(a2 - a) > 0.02 or abs(b2 - b) > 0.02:
                moved.append((bi, a, b, a2, b2))
            if out and a2 <= out[-1][1] + 0.02:
                out[-1][1] = max(out[-1][1], b2)
            else:
                out.append([a2, b2])
        bl["src"] = out
    json.dump(e, open(dst, "w"), ensure_ascii=False, indent=1)
    if "--report" in sys.argv:
        for bi, a, b, a2, b2 in moved:
            print(f"b{bi:<2d} [{a:.2f}, {b:.2f}] -> [{a2:.2f}, {b2:.2f}]  (+{b2 - b:.2f}s end, {a2 - a:+.2f}s start)")
    print(f"{len(moved)} edges snapped")


if __name__ == "__main__":
    main()
