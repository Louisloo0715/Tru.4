#!/usr/bin/env python3
"""Remove stretches of the *finished* timeline from an EDL (tighten an edit after watching it).

usage: python3 -I cut_edl.py edl_in.json edl_out.json subs_out.json  a-b [a-b ...]
  a-b = output-time ranges (seconds, from the current cut) to delete.
Block source ranges are re-split; the subtitle file (edl["subs_file"]) and the shot list are shifted to the new
timeline (items inside a removed range are dropped). Cards / SFX are source-time based and follow automatically.
"""
import copy, json, os, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ghost  # noqa: E402


def main():
    src_p, dst_p, subs_out = sys.argv[1:4]
    R = sorted(tuple(float(x) for x in r.split("-")) for r in sys.argv[4:])
    e = json.load(open(src_p))
    w = wave.open(e["audio"]); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    if w.getnchannels() > 1:
        v = v.reshape(-1, w.getnchannels()).mean(1)
    old = ghost.Timeline(copy.deepcopy(e), v)

    def removed_before(t):
        return sum(min(b, t) - a for a, b in R if a < t)

    def inside(t):
        return any(a <= t < b for a, b in R)

    def remap(t):
        for a, b in R:
            if a <= t < b:
                t = a
        return round(t - removed_before(t), 3)

    new_blocks = []
    for bi, bl in enumerate(e["blocks"]):
        if "gap" in bl:
            new_blocks.append(bl); continue
        keep = []
        for t0, a, b, pbi in old.pieces:
            if pbi != bi:
                continue
            segs = [(t0, t0 + (b - a))]
            for ra, rb in R:
                nxt = []
                for s0, s1 in segs:
                    if rb <= s0 or ra >= s1:
                        nxt.append((s0, s1)); continue
                    if s0 < ra:
                        nxt.append((s0, ra))
                    if rb < s1:
                        nxt.append((rb, s1))
                segs = nxt
            keep += [[a + (s0 - t0), a + (s1 - t0)] for s0, s1 in segs if s1 - s0 > 0.04]
        if keep:
            nb = dict(bl); nb["src"] = keep; new_blocks.append(nb)
        else:
            print(f"block {bi} removed entirely", file=sys.stderr)
    e["blocks"] = new_blocks

    subs = json.load(open(e["subs_file"]))
    ns = [[remap(a), remap(b), t] for a, b, t in subs if not inside((a + b) / 2)]
    json.dump(ns, open(subs_out, "w"), ensure_ascii=False, indent=0)
    e["subs_file"] = os.path.abspath(subs_out)

    shots, seen = [], {}
    for t, want, fb in sorted(e.get("shots", []), key=lambda x: x[0]):
        seen[remap(t)] = [remap(t), want, fb]  # a shot starting inside a cut lands on the cut point; last one wins
    e["shots"] = sorted(seen.values(), key=lambda x: x[0])
    json.dump(e, open(dst_p, "w"), ensure_ascii=False, indent=1)
    new = ghost.Timeline(copy.deepcopy(e), v)
    print(f"{old.dur:.1f}s -> {new.dur:.1f}s (removed {sum(b - a for a, b in R):.1f}s in {len(R)} cuts)")


if __name__ == "__main__":
    main()
