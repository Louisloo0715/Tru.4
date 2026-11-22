"""v4 sound pass for 半夜坐錯車 (user: "BGM 沒聽到，也沒有音效，陰森感不夠").
Swaps in the phone-audible eerie BGM and gives every story block real SFX at audible levels.
usage: python3 -I patch_v4.py SCRATCH   (edl_v3.json -> edl_v4.json; subtitles are re-aligned separately)"""
import json, sys
E = sys.argv[1] + "/ep2/"
e = json.load(open(E + "edl_v3.json"))
e["music"] = E + "music/bgm_eerie.wav"
S = lambda kind, db, t=None, src_t=None: dict(kind=kind, db=db, **({"t": t} if t is not None else {"src_t": src_t}))
SFX = {  # block index -> full sfx list
    0: [S("riser", -4, t=0), S("whisper", -8, t=0.3), S("stinger", -2, src_t=468.3)],
    2: [S("buzz", -8, t=0)],
    3: [S("whoosh", -6, t=0)],
    4: [S("whoosh", -8, t=0), S("hit", -10, t=0.05)],
    5: [S("whoosh", -8, t=0)],
    6: [S("reverse", -6, src_t=103.7)],
    8: [S("reverse", -8, src_t=139.5), S("hit", -6, src_t=140.0)],
    9: [S("car_door", -1, src_t=148.4)],
    10: [S("whisper", -10, src_t=157.0), S("hit", -10, src_t=158.0)],
    12: [S("riser", -5, src_t=185.0)],
    13: [S("reverse", -8, src_t=195.6)],
    15: [S("riser", -6, t=4.0)],
    16: [S("hit", 0, src_t=258.8), S("stinger", -3, src_t=258.9), S("whisper", -6, t=1.5)],
    17: [S("owl", -10, t=3.0), S("whisper", -10, t=8.0)],
    19: [S("reverse", -2, src_t=315.8), S("stinger", 0, src_t=317.3)],
    20: [S("vibrate", -2, src_t=326.5), S("stinger", -4, src_t=329.1)],
    21: [S("ringback", -6, src_t=333.4)],
    23: [S("riser", -8, src_t=375.5)],
    24: [S("hit", -8, src_t=391.3)],
    27: [S("whoosh", -8, t=0), S("reverse", -8, t=4.0)],
    28: [S("whisper", -6, t=0.5), S("reverse", -2, src_t=461.0), S("stinger", 0, src_t=468.3)],
    30: [S("hit", -5, src_t=519.5)],
    31: [S("riser", -6, src_t=537.5)],
    32: [S("reverse", -2, src_t=545.5), S("whisper", -6, t=0.2), S("car_door", 0, src_t=548.3)],
    33: [S("hit", -4, src_t=554.0), S("stinger", 0, src_t=554.0)],
    34: [S("whoosh", -8, t=0)],
}
AMB = {5: dict(amb_city=-22), 7: dict(amb_city=-22), 8: dict(amb_city=-22), 9: dict(amb_city=-24),
       10: dict(amb_car=-16), 11: dict(amb_car=-16), 12: dict(amb_car=-20), 13: dict(amb_car=-16), 14: dict(amb_car=-18),
       15: dict(amb_car=-16), 16: dict(amb_crickets=-20, amb_wind=-26), 17: dict(amb_crickets=-20, amb_wind=-24),
       18: dict(amb_car=-20), 19: dict(amb_car=-20), 20: dict(amb_car=-20), 21: dict(amb_car=-20), 22: dict(amb_car=-22),
       23: dict(amb_car=-24)}
for i, b in enumerate(e["blocks"]):
    if i in SFX: b["sfx"] = SFX[i]
    if i in AMB:
        for k in [k for k in b if k.startswith("amb_")]: del b[k]
        b.update(AMB[i])
for i in (13, 31):
    e["blocks"][i].update(heartbeat=True, heartbeat_bpm=62 if i == 13 else 72)
json.dump(e, open(E + "edl_v4.json", "w"), ensure_ascii=False, indent=1)
print("v4:", sum(len(v) for v in SFX.values()), "sfx in", len(SFX), "blocks")
