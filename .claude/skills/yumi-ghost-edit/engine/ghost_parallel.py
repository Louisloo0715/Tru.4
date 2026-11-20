#!/usr/bin/env python3
"""Render a ghost EDL in N parallel chunks, then mux with the mix.
usage: python3 -I ghost_parallel.py edl.json out.mp4 [N=4] [--reuse-video]   (re-mix audio only with --reuse-video)"""
import json, os, subprocess, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ghost
edl_p, out = sys.argv[1], sys.argv[2]
N = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 4
reuse = "--reuse-video" in sys.argv
edl = json.load(open(edl_p))
w = wave.open(edl["audio"]); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
tl = ghost.Timeline(edl, v)
base = os.path.splitext(out)[0]
vid = base + "_video.mp4"
eng = os.path.join(HERE, "ghost.py")
procs = []
if not reuse:
    step = tl.n / N
    parts = []
    for i in range(N):
        a, b = round(i * step) / ghost.FPS, round((i + 1) * step) / ghost.FPS
        pth = f"{base}_part{i}.mp4"; parts.append(pth)
        procs.append(subprocess.Popen(["python3", "-I", eng, edl_p, pth, "--video-only", "--range", f"{a},{b}"],
                                      stdout=subprocess.DEVNULL, stderr=open(f"{base}_part{i}.log", "w")))
aud = base + "_mix.wav"
pa = subprocess.Popen(["python3", "-I", eng, edl_p, aud, "--audio-only"], stdout=subprocess.DEVNULL, stderr=open(base + "_audio.log", "w"))
for p in procs + [pa]:
    p.wait()
    if p.returncode:
        sys.exit(f"a render process failed ({p.args[-1]}); see logs next to {out}")
if not reuse:
    lst = base + "_parts.txt"
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid], check=True)
    for p in parts:
        os.remove(p)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", aud, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
print(f"done {tl.dur:.1f}s -> {out}")
