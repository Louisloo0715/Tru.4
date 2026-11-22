"""Edit of 《半夜坐錯車…司機把我載去墓地》 for 玉米講鬼 TALK (16:9).
usage: python3 -I build_edl.py SCRATCH   (SCRATCH holds ep2/ with a48.wav, transcript.json, music/, user_new/)

A first-person story (玉米 himself, Kuala Lumpur, a Grab ride at 1 AM). Less monster horror, more "wait... then who
booked the cemetery?" — so: light stays mid until the cemetery reveal, a comic 烏龍 beat sits right before the twist
(see SKILL.md comedy rule), and the ending line "在他們的世界也可以叫 Grab" gets the last stinger.
"""
import json, sys, os
SP = sys.argv[1]; E = SP + "/ep2"; G1 = SP + "/ghost"
SK = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
W = lambda s: [s, "w"]; R = lambda s: [s, "r"]


def blk(src, mode="host", **k):
    d = dict(src=src if isinstance(src[0], list) else [src], mode=mode); d.update(k); return d


def sfx(kind, t=None, src_t=None, db=0):
    d = dict(kind=kind, db=db)
    if t is not None: d["t"] = t
    else: d["src_t"] = src_t
    return d


def card(src_t, lines, hold="block"): return dict(src_t=src_t, lines=lines, hold=hold)


fixes = {"GRAD": "Grab", "GRA D": "Grab", "上坐車": "上錯車", "時機": "司機", "位置來電": "未接來電", "是水啊": "是誰啊",
         "埋人": "馬來人", "大屋農": "大烏龍", "大武龍": "大烏龍", "烤牙": "靠腰", "玉米中": "玉米就", "媽媽烈烈": "罵罵咧咧",
         "習慣是": "奇怪的是", "論了一下": "愣了一下", "目的去了": "墓地去了", "實際": "司機", "買我的聲音": "用馬來文",
         "兩車": "輛車", "跳這一個": "聽到這個"}

blocks = [
    # ---------------- cold open: ONE line, then title
    blk([462.1, 469.4], "black", light=0.95, dread=0.9, pip=True, trans="fade", music_at=118, music_db=-5, amb_car=-30,
        cards=[card(462.2, [W("是誰…")], 1.0), card(463.1, [W("在三更半夜")], 3.4), card(466.6, [R("要司機送他去墓地？")])],
        sfx=[sfx("riser", t=0, db=-8), sfx("stinger", src_t=468.3, db=-4)]),
    dict(gap=3.2, mode="black", light=1.0, dread=1, pip=False, music_db=-4,
         title=dict(line1="半夜坐錯車", line2="司機把我載去墓地？！", strip="玉米親身經歷"),
         sfx=[sfx("hit", t=0, db=3), sfx("stinger", t=0.05, db=-6)], fade_out=True),
    # ---------------- host intro (comic: lazy 玉米 always calls Grab)
    blk([[3.1, 4.6], [11.6, 16.8], [18.9, 25.4]], max_pause=0.35, light=0.0, dread=0.1, zoom=[1.0, 1.04], trans="flicker",
        music_at=0, music_db=-6, amb_room=-32, sfx=[sfx("buzz", t=0, db=-10)]),
    blk([[36.8, 38.6], [39.0, 43.6], [45.6, 55.3], [55.7, 61.6]], max_pause=0.4, light=0.15, dread=0.3, zoom=[1.15, 1.25],
        music_db=-5, amb_room=-32, sfx=[sfx("whoosh", t=0, db=-12)]),
    # ---------------- 1 AM, waiting for the Grab
    blk([[62.8, 70.9], [71.7, 76.9], [77.7, 81.9], [82.0, 85.5], [92.2, 96.0]], "broll", max_pause=0.45, light=0.3, dread=0.35,
        trans="fade", music_db=-6, amb_city=-28),
    blk([[98.5, 102.0], [102.0, 105.0]], max_pause=0.6, light=0.35, dread=0.45, zoom=[1.2, 1.3], music_db=-5, amb_room=-32,
        sfx=[sfx("reverse", src_t=103.7, db=-10)]),
    blk([[120.1, 125.6], [129.4, 132.7]], "broll", max_pause=0.5, light=0.35, dread=0.4, music_db=-6, amb_city=-26),
    blk([[135.2, 141.3]], "broll", max_pause=0.6, light=0.4, dread=0.45, music_db=-6, amb_city=-26,
        cards=[card(140.0, [W("車牌："), R("5124")])], sfx=[sfx("hit", src_t=140.0, db=-12)]),
    blk([[144.4, 148.6]], "broll", max_pause=0.5, light=0.4, dread=0.45, music_db=-6, amb_city=-28,
        sfx=[sfx("car_door", src_t=148.4, db=-4)]),
    # ---------------- inside the car: the driver asks nothing
    blk([[150.6, 158.3], [158.8, 161.6], [166.6, 168.1]], "broll", max_pause=0.7, light=0.5, dread=0.55, trans="cut",
        music_at=70, music_db=-5, amb_car=-20),
    blk([[172.3, 182.3]], "broll", max_pause=0.6, light=0.5, dread=0.5, music_db=-6, amb_car=-20),
    blk([[183.0, 187.9]], max_pause=0.8, light=0.6, dread=0.65, zoom=[1.2, 1.32], music_db=-5, amb_car=-24,
        sfx=[sfx("riser", src_t=185.0, db=-10)]),
    blk([[188.8, 189.1], [191.4, 194.1], [195.6, 198.1]], "broll", max_pause=0.7, light=0.65, dread=0.65, music_db=-5, amb_car=-20),
    blk([[206.2, 211.2], [228.2, 228.7], [230.2, 233.8]], max_pause=0.5, light=0.55, dread=0.55, zoom=[1.0, 1.08],
        music_db=-6, amb_car=-24),
    blk([[244.5, 252.0]], "broll", max_pause=0.8, light=0.75, dread=0.75, music_db=-5, amb_car=-20, heartbeat=True, heartbeat_bpm=64),
    # ---------------- the reveal
    blk([[253.7, 256.9], [257.3, 259.6]], "broll", max_pause=1.0, light=0.85, dread=0.95, trans="flash", music_at=118, music_db=-4,
        amb_crickets=-26, cards=[card(258.2, [R("這不是墓園嗎？")])],
        sfx=[sfx("hit", src_t=258.8, db=-2), sfx("stinger", src_t=258.9, db=-6)]),
    blk([[267.5, 269.2], [275.9, 287.9]], "broll", max_pause=0.6, light=0.8, dread=0.85, music_db=-5, amb_crickets=-26, amb_wind=-30),
    blk([[292.7, 294.1], [296.6, 301.8]], max_pause=0.7, light=0.8, dread=0.85, zoom=[1.2, 1.35], trans="flicker", music_db=-5,
        amb_car=-26, heartbeat=True, heartbeat_bpm=72),
    blk([[307.3, 309.2], [314.9, 317.8]], "broll", max_pause=1.1, light=0.95, dread=1, music_db=-4, amb_car=-24,
        heartbeat=True, heartbeat_bpm=80,
        cards=[card(314.9, [W("你的 APP 設的目的地…")], 2.4), card(317.3, [R("就是這裡")])],
        sfx=[sfx("reverse", src_t=315.8, db=-4), sfx("stinger", src_t=317.3, db=-3)]),
    # ---------------- the phone
    blk([[320.2, 323.6], [324.6, 331.0]], "broll", max_pause=0.6, light=0.7, dread=0.7, trans="cut", music_at=70, music_db=-5,
        amb_car=-24, sfx=[sfx("vibrate", src_t=326.5, db=-8)], cards=[card(329.1, [R("7 通未接來電")])]),
    blk([[332.2, 337.2], [338.0, 344.3]], "broll", max_pause=0.6, light=0.7, dread=0.7, music_db=-6, amb_car=-24,
        sfx=[sfx("ringback", src_t=333.4, db=-14)]),
    blk([[355.6, 364.8]], "broll", max_pause=0.5, light=0.7, dread=0.7, music_db=-6, amb_car=-26,
        voice_fx=[dict(src=[355.5, 364.9], fx="phone")]),
    blk([[367.3, 376.8]], max_pause=0.6, light=0.6, dread=0.6, zoom=[1.1, 1.2], music_db=-6, amb_car=-28),
    # ---------------- comic beat: 烏龍 (relax right before the twist)
    blk([[380.0, 383.5], [390.7, 392.1]], max_pause=0.6, light=0.05, dread=0.05, zoom=[1.3, 1.35], trans="flicker", music_at=0,
        music_db=-7, amb_room=-32, cards=[card(390.7, [R("上錯車了！")])], sfx=[sfx("hit", src_t=391.3, db=-12)]),
    blk([[393.5, 395.2], [397.96, 399.8], [400.7, 407.2], [408.0, 410.6]], "broll", max_pause=0.5, light=0.1, dread=0.05,
        music_db=-7, amb_room=-34, cards=[card(404.0, [W("要搭："), W("5142")], 2.0), card(406.2, [W("上了："), R("5124")])]),
    blk([[413.6, 417.5], [421.6, 425.3], [430.0, 435.0], [435.6, 437.5], [439.4, 442.1], [443.4, 445.1]], max_pause=0.45,
        light=0.05, dread=0.05, zoom=[1.0, 1.05], music_db=-8, amb_room=-32),
    # ---------------- the twist
    blk([[446.0, 452.6]], "broll", max_pause=0.9, light=0.6, dread=0.6, trans="fade", music_at=118, music_db=-6, amb_room=-30),
    blk([[454.5, 455.3], [456.9, 460.1], [461.2, 469.4]], "black", max_pause=1.3, light=1.0, dread=1, pip=True, heartbeat=True,
        heartbeat_bpm=86, music_db=-4,
        cards=[card(456.9, [W("如果我上錯車了…")], 3.2), card(462.2, [W("那麼是誰")], 1.2), card(463.1, [W("在三更半夜")], 3.4),
               card(466.6, [R("要司機送他去墓地？")])],
        sfx=[sfx("reverse", src_t=461.0, db=-4), sfx("stinger", src_t=468.3, db=-2)]),
    blk([[480.7, 482.9], [485.1, 486.4], [487.0, 487.5], [488.3, 491.4], [492.2, 494.2]], max_pause=0.8, light=0.75, dread=0.75,
        zoom=[1.1, 1.2], music_db=-5, amb_room=-30),
    blk([[495.4, 497.7], [500.7, 503.9], [508.3, 512.3], [513.2, 514.4], [515.2, 517.4], [518.6, 521.3]], "broll", max_pause=0.7,
        light=0.75, dread=0.75, music_db=-5, amb_room=-30, cards=[card(518.6, [R("付了兩次錢")])],
        sfx=[sfx("hit", src_t=519.5, db=-10)]),
    blk([[529.3, 531.5], [533.8, 534.7], [535.4, 540.0]], max_pause=0.8, light=0.85, dread=0.85, zoom=[1.2, 1.32], music_db=-5),
    blk([[542.1, 542.9], [545.7, 548.5]], "black", max_pause=1.2, light=1.0, dread=1, pip=True, heartbeat=True, heartbeat_bpm=90,
        music_db=-4, cards=[card(545.7, [W("玉米上車啊…")], 0.9), card(546.6, [R("他也上車了呢")])],
        sfx=[sfx("reverse", src_t=545.5, db=-4), sfx("car_door", src_t=548.3, db=-3)]),
    blk([[550.1, 551.7], [552.9, 555.2]], "broll", max_pause=1.0, light=0.95, dread=1, music_db=-4,
        cards=[card(552.9, [W("在他們的世界")], 1.1), card(554.0, [R("也可以叫 Grab")])], sfx=[sfx("stinger", src_t=554.0, db=-2)]),
    # ---------------- outro
    blk([[556.9, 558.9], [561.0, 567.0], [584.1, 587.4]], max_pause=0.4, light=0.0, dread=0.1, zoom=[1.0, 1.03], trans="flicker",
        music_at=0, music_db=-8, amb_room=-32, fade_out=True),
]
ep1 = json.load(open(SK + "/episodes/黃皮子討封/edl_v12.json"))
edl = dict(audio=E + "/a48.wav", transcript=E + "/transcript.json", music=E + "/music/bgm_urban.wav",
           assets=dict(room=SK + "/assets/studio/room.webp", desk=SK + "/assets/studio/desk.webp", sprites=SK + "/assets/mascot"),
           fixes=fixes, blocks=blocks, vecteezy_dir=E + "/user_new", broll_dir=G1 + "/broll",
           sfx_files={k: v for k, v in ep1["sfx_files"].items() if k in ("hit", "riser", "reverse")},
           heartbeat_file=ep1["heartbeat_file"])
json.dump(edl, open(E + "/edl_v1.json", "w"), ensure_ascii=False, indent=1)
print(len(blocks), "blocks")
