"""v7 scare/comedy pass for 半夜坐錯車 (user: "沒有很可怕，BGM 不明顯，後面也沒有突然轉搞笑的感覺").
- story blocks: music +4 dB (≈7 dB under the voice instead of ≈11)
- "calm before the scare": the block right before each big scare drops the music to a whisper (heartbeat only),
  the scare block slams back at full level with hit + stinger
- comedy switch: record scratch kills the horror music, a bouncy comic loop (amb_comic) plays, boing on the punchline;
  "可是 回到家…" cuts the comedy off and drops straight back into the dark
usage: python3 -I patch_v7.py SCRATCH   (edl_v6.json -> edl_v7.json)"""
import json, sys
E = sys.argv[1] + "/ep2/"
e = json.load(open(E + "edl_v6.json")); B = e["blocks"]
S = lambda kind, db, t=None, src_t=None: dict(kind=kind, db=db, **({"t": t} if t is not None else {"src_t": src_t}))
e["drone_db"] = -19
for i, b in enumerate(B):
    if b.get("dread", 0) >= 0.5 and "music_db" in b:
        b["music_db"] = min(0, b["music_db"] + 4)
DIP = {15: -14, 18: -12, 27: -16, 31: -12}           # calm before the scare
SLAM = {16: 0, 19: 0, 28: 0, 32: 0, 33: 0}            # the scare itself
for i, v in DIP.items(): B[i]["music_db"] = v; B[i]["heartbeat"] = True; B[i].setdefault("heartbeat_bpm", 70)
for i, v in SLAM.items(): B[i]["music_db"] = v
# comedy switch (blocks 24-26)
for i in (24, 25, 26):
    B[i]["music_db"] = -40; B[i]["amb_comic"] = -9; B[i]["dread"] = 0.0
    for k in [k for k in B[i] if k.startswith("amb_") and k != "amb_comic"]: del B[i][k]
B[24]["sfx"] = [S("scratch", 2, t=0.0), S("boing", -3, src_t=391.3)]
B[25]["sfx"] = [S("boing", -6, src_t=406.4)]
B[27]["sfx"] = [S("hit", -4, t=0.0), S("reverse", -6, t=3.0)]

json.dump(e, open(E + "edl_v7.json", "w"), ensure_ascii=False, indent=1)
print("v7 written")
