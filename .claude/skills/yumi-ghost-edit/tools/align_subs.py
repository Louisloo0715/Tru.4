#!/usr/bin/env python3
"""Re-time hand-corrected subtitles to the FINISHED voice track (user: "字幕後面開始亂掉了，跟著說話出字").

usage: python3 -I align_subs.py subs_in.json cut_words.json subs_out.json [--report]
  subs_in    [[t0, t1, text], ...]  corrected text (times may be stale/approximate)
  cut_words  [{"s","e","w"}, ...]   faster-whisper word timestamps of the rendered voice (STEMS_DIR voice.wav)
Matching is done on toneless pinyin (robust to simplified/traditional and homophone ASR errors); digits are read as
Chinese numerals, latin words lowercased. Each line starts at its first spoken syllable and stays up until its last
syllable ends (+0.3 s, never past the next line), minimum 0.7 s on screen.
"""
import json, re, sys
from difflib import SequenceMatcher
from pypinyin import lazy_pinyin

DIG = dict(zip("0123456789", ["ling", "yi", "er", "san", "si", "wu", "liu", "qi", "ba", "jiu"]))


def toks(text):
    out = []
    for m in re.finditer(r"[A-Za-z]+|\d|[一-鿿]", text):
        s = m.group(0)
        if s.isdigit(): out.append(DIG[s])
        elif s.isascii(): out.append(s.lower())
        else: out.append(lazy_pinyin(s)[0])
    return out


def main():
    subs = json.load(open(sys.argv[1])); words = json.load(open(sys.argv[2]))
    A, AT = [], []  # asr tokens and their (start, end)
    for w in words:
        tk = toks(w["w"])
        if not tk: continue
        d = (w["e"] - w["s"]) / len(tk)
        for i, x in enumerate(tk):
            A.append(x); AT.append((w["s"] + i * d, w["s"] + (i + 1) * d))
    S, SI = [], []
    for k, (_, _, t) in enumerate(subs):
        for x in toks(t.replace("{", "").replace("}", "")):
            S.append(x); SI.append(k)
    sm = SequenceMatcher(None, S, A, autojunk=False)
    hit = {}
    for a, b, n in sm.get_matching_blocks():
        for j in range(n):
            hit[a + j] = b + j
    out = []
    for k, (t0, t1, text) in enumerate(subs):
        idx = [i for i, s in enumerate(SI) if s == k]
        m = [hit[i] for i in idx if i in hit]
        cov = len(m) / max(1, len(idx))
        if m:
            out.append([AT[m[0]][0], AT[m[-1]][1], text, cov])
        else:
            out.append([None, None, text, 0.0])
    # fill unmatched by interpolation between neighbours
    for k, o in enumerate(out):
        if o[0] is None:
            prev = next((out[j][1] for j in range(k - 1, -1, -1) if out[j][1] is not None), 0.0)
            nxt = next((out[j][0] for j in range(k + 1, len(out)) if out[j][0] is not None), prev + 1.5)
            o[0], o[1] = prev + 0.05, max(prev + 0.8, nxt - 0.05)
    res = []
    for k, (a, b, text, cov) in enumerate(out):
        nxt = out[k + 1][0] if k + 1 < len(out) else b + 1.0
        a = max(0.0, a - 0.05)
        end = min(max(b + 0.3, a + 0.7), max(nxt - 0.02, b))
        res.append([round(a, 2), round(end, 2), text])
        if "--report" in sys.argv and cov < 0.6:
            print(f"low match {cov:.0%}: {a:7.2f} {text}")
    json.dump(res, open(sys.argv[3], "w"), ensure_ascii=False, indent=0)
    print(f"{len(res)} lines aligned; {sum(1 for o in out if o[3] >= 0.6)} with >=60% syllables matched")


if __name__ == "__main__":
    main()
