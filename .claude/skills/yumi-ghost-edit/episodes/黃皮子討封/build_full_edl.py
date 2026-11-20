"""Full edit of 【民間怪談】黃鼠狼討封 for 玉米講鬼 TALK (16:9)."""
import json, sys
SP = sys.argv[1]; G = SP + "/ghost"; B = G + "/broll/"; IMG = SP + "/../images/"
W = lambda s: [s, "w"]; R = lambda s: [s, "r"]
def c(name, start=0, red=False): return dict(file=B + name + ".mp4", start=start, red=red)
def blk(src, mode="host", **k):
    d = dict(src=src if isinstance(src[0], list) else [src], mode=mode); d.update(k); return d
def sfx(kind, t=None, src_t=None, db=0):
    d = dict(kind=kind, db=db)
    if t is not None: d["t"] = t
    else: d["src_t"] = src_t
    return d
def card(src_t, lines, hold="block"): return dict(src_t=src_t, lines=lines, hold=hold)

fixes = json.load(open(G + "/edl_A2.json"))["fixes"]
fixes.update({"這下一秒": "下一秒", "大怪風": "怪風", "不要找安齊天": "不要找俺", "安齊天": "俺", "幫他瘋了": "幫他封了",
              "你到底撤瘋了": "你到底封了", "撤瘋了": "封了", "就似乎你怎樣": "就是看你怎樣", "一隻一句的縮": "一字一句的說",
              "英國": "因果", "縮": "說", "應該被黃鼠狼": "應該是被黃鼠狼", "瘋瘋癲癲": "瘋瘋癲癲"})

blocks = [
    # ---------------- cold open
    blk([471.4, 476.3], "broll", brolls=[c("ferret", 1, True)], light=0.9, dread=0.9, pip=False, trans="fade",
        music_at=118, music_db=-17, amb_wind=-26,
        cards=[card(471.5, [W("你看我…")], 1.2), card(472.7, [W("像人…")], 1.5), card(474.4, [R("還是像神？")])],
        sfx=[sfx("riser", t=0, db=-8), sfx("whisper", t=0.2, db=-8)]),
    blk([600.2, 605.4], "broll", brolls=[c("fog", 3), c("moonclouds", 6)], light=0.95, dread=1, pip=False, trans="flicker",
        music_db=-15, amb_wind=-22, cards=[card(600.3, [W("你知道…")], 1.6), card(603.1, [R("你在說什麼嗎？")])],
        sfx=[sfx("reverse", src_t=601.6, db=-6), sfx("stinger", src_t=603.1, db=-4)]),
    dict(gap=3.2, mode="broll", broll=c("fogforest", 1), light=1.0, dread=1, pip=False, music_db=-14, amb_wind=-26,
         title=dict(line1="黃皮子討封", line2="封成孫悟空？！", strip="有人真的這樣回答…"),
         sfx=[sfx("hit", t=0, db=3), sfx("stinger", t=0.05, db=-6)], fade_out=True),
    # ---------------- host intro
    blk([0.9, 8.62], max_pause=0.35, light=0.0, dread=0.15, zoom=[1.0, 1.04], trans="flicker", music_at=0, music_db=-24, amb_room=-32,
        sfx=[sfx("buzz", t=0, db=-10)]),
    blk([46.3, 50.0], max_pause=0.35, light=0.05, dread=0.25, zoom=[1.2, 1.26], music_db=-22, amb_room=-32, sfx=[sfx("whoosh", t=0, db=-12)]),
    blk([297.4, 309.6], "broll", max_pause=0.4, brolls=[c("fogforest", 0), c("grass", 2), c("moonforest", 0)], light=0.35, dread=0.4,
        music_db=-20, amb_wind=-24, amb_crickets=-30, sfx=[sfx("whoosh", t=0, db=-10), sfx("owl", t=2.5, db=-10)]),
    blk([310.0, 316.4], "broll", max_pause=0.8, brolls=[c("ferret", 2, True)], light=0.5, dread=0.55, music_db=-19, amb_wind=-24,
        cards=[card(310.1, [W("你覺得我像人嗎…")], 3.1), card(313.3, [R("還是像神呢？")])],
        sfx=[sfx("rustle", t=0, db=-8), sfx("hit", src_t=313.3, db=-8)]),
    blk([348.9, 355.8], max_pause=0.4, light=0.3, dread=0.35, zoom=[1.0, 1.06], music_db=-22, amb_room=-32),
    blk([361.3, 373.1], max_pause=0.45, light=0.45, dread=0.55, zoom=[1.15, 1.32], music_db=-20, amb_room=-30,
        sfx=[sfx("riser", src_t=365.0, db=-12)]),
    # ---------------- story part 1
    blk([418.3, 432.1], "broll", max_pause=0.55, brolls=[c("manfog", 1), c("forestwalk", 3), c("moonforest", 0), c("feet", 4)],
        light=0.6, dread=0.6, trans="fade", music_at=75, music_db=-19, amb_crickets=-26, amb_wind=-27,
        sfx=[sfx("hit", t=0, db=-10), sfx("footsteps", t=1.0, db=-7), sfx("owl", t=8, db=-12)]),
    blk([432.7, 437.6], "broll", max_pause=0.6, brolls=[c("feet", 10), c("forestwalk", 9)], light=0.7, dread=0.65, music_db=-19,
        amb_crickets=-26, amb_wind=-27, sfx=[sfx("footsteps", t=0, db=-5)]),
    blk([437.6, 448.1], max_pause=0.6, light=0.6, dread=0.7, zoom=[1.1, 1.25], music_db=-18, amb_crickets=-34, sfx=[sfx("rustle", t=1.0, db=-10)]),
    blk([456.5, 465.1], "broll", max_pause=0.6, brolls=[c("moonforest", 0), c("grass", 8), c("fog", 9)], light=0.75, dread=0.75,
        music_db=-17, amb_wind=-28, sfx=[sfx("rustle", t=2.0, db=-8)]),
    blk([465.7, 469.7], max_pause=0.9, light=0.8, dread=0.85, zoom=[1.35, 1.45], trans="flicker", heartbeat=True, heartbeat_bpm=70,
        music_db=-15, sfx=[sfx("buzz", t=0, db=-8), sfx("reverse", src_t=468.0, db=-5)]),
    blk([471.4, 476.4], "broll", max_pause=0.9, brolls=[c("ferret", 0, True)], light=0.9, dread=1, heartbeat=True, heartbeat_bpm=78,
        music_db=-14, amb_wind=-30,
        cards=[card(471.5, [W("你看我…")], 1.2), card(472.7, [W("像人…")], 1.5), card(474.4, [R("還是像神？")])],
        sfx=[sfx("whisper", t=0.3, db=-6), sfx("stinger", src_t=474.4, db=-3)]),
    blk([479.6, 494.0], max_pause=0.5, light=0.65, dread=0.6, zoom=[1.0, 1.08], music_db=-19, amb_crickets=-34),
    blk([494.4, 510.4], "broll", max_pause=0.5, brolls=[c("manfog", 8), c("feet", 15), c("forestwalk", 14)], light=0.65, dread=0.6,
        music_db=-19, amb_crickets=-28, amb_wind=-28),
    blk([513.4, 519.4], "broll", max_pause=0.7, brolls=[c("ferret", 3, True), c("grass", 12)], light=0.75, dread=0.7, music_db=-18,
        amb_wind=-28, cards=[card(516.9, [W("你…不像人")])], sfx=[sfx("hit", src_t=518.3, db=-10)]),
    blk([520.5, 528.6], max_pause=0.8, light=0.7, dread=0.7, zoom=[1.2, 1.32], music_db=-17,
        cards=[card(526.0, [R("你…也不像神")])], sfx=[sfx("hit", src_t=527.0, db=-8)]),
    blk([529.5, 542.0], "broll", max_pause=0.9, brolls=[c("fog", 0), c("ferret", 5, True), c("moonclouds", 12)], light=0.85, dread=0.85,
        music_db=-16, amb_wind=-26, heartbeat=True, heartbeat_bpm=66,
        cards=[card(537.7, [W("我像人…")], 2.0), card(539.7, [R("還是像神呢？")])],
        sfx=[sfx("whisper", src_t=533.0, db=-10), sfx("stinger", src_t=539.7, db=-6)]),
    # ---------------- climax
    blk([547.4, 551.5], max_pause=1.2, light=0.65, dread=0.7, zoom=[1.05, 1.12], trans="fade", music_at=100, music_db=-23),
    blk([552.0, 557.4], "broll", max_pause=0.6, brolls=[c("manfog", 2), c("feet", 20)], light=0.7, dread=0.7, music_db=-18,
        amb_crickets=-30, amb_wind=-28),
    blk([557.4, 562.0], max_pause=0.7, light=0.6, dread=0.75, zoom=[1.3, 1.38], music_db=-16,
        cards=[card(559.5, [R("孫悟空")])], sfx=[sfx("hit", src_t=559.5, db=-4)]),
    blk([565.0, 575.0], "broll", max_pause=0.9, brolls=[c("wind", 4), c("lightning", 6), c("wind", 18)], light=0.85, dread=0.95,
        trans="flash", music_db=-15, amb_storm=-9,
        sfx=[sfx("whoosh", src_t=569.1, db=0), sfx("hit", src_t=569.2, db=-6), sfx("gust", t=0.4, db=-2), sfx("crack", t=4.5, db=-4)]),
    blk([576.5, 597.2], "broll", max_pause=1.3, brolls=[c("ferret", 0, True), c("fog", 5), c("moonclouds", 2), c("grass", 15)],
        light=0.9, dread=1, heartbeat=True, heartbeat_bpm=60, music_at=118, music_db=-18, amb_wind=-26,
        sfx=[sfx("rustle", t=3, db=-8), sfx("whisper", t=11, db=-10)]),
    blk([600.2, 605.4], "black", max_pause=1.2, light=1.0, dread=1, pip=True, heartbeat=True, heartbeat_bpm=78, music_db=-13,
        cards=[card(600.3, [W("你知道…")], 2.0), card(603.1, [R("你在說什麼嗎？")])],
        sfx=[sfx("reverse", src_t=601.5, db=-4), sfx("stinger", src_t=603.1, db=-2)]),
    blk([608.8, 624.8], max_pause=0.8, light=0.75, dread=0.8, zoom=[1.1, 1.2], trans="flicker", music_db=-18, amb_room=-30),
    blk([630.4, 642.0], "broll", max_pause=1.0, brolls=[c("ferret", 4, True), c("fog", 12), c("grass", 4)], light=0.9, dread=0.95,
        music_db=-16, amb_wind=-26, sfx=[sfx("rustle", t=1.5, db=-6), sfx("reverse", src_t=642.0, db=-5)]),
    blk([[643.8, 649.1], [650.5, 656.4]], "broll", max_pause=0.9, brolls=[c("moonclouds", 6), c("fog", 2)], light=0.95, dread=1,
        trans="flicker", music_db=-14, amb_wind=-24,
        cards=[card(643.9, [W("有些名字"), R("不能亂講")], 4.0), card(650.6, [W("有些因果"), R("也不能亂背")])],
        sfx=[sfx("hit", src_t=647.3, db=-2), sfx("hit", src_t=654.1, db=-4)]),
    blk([660.6, 671.4], "broll", max_pause=0.8, brolls=[c("feet", 8), c("grass", 0), c("forestwalk", 16)], light=0.85, dread=0.95,
        heartbeat=True, heartbeat_bpm=96, music_db=-16, amb_wind=-26),
    blk([672.4, 694.8], "broll", max_pause=1.1, brolls=[c("ferret", 1, True), c("moonclouds", 15), c("fog", 7)], light=1.0, dread=1,
        heartbeat=True, heartbeat_bpm=84, music_at=125, music_db=-15, amb_wind=-28,
        cards=[card(680.9, [W("你給了我")], 3.0), card(684.1, [R("承受不起的因果")], 3.4),
               card(687.7, [W("這份因果")], 2.8), card(690.6, [R("就由你…替我還吧")])],
        sfx=[sfx("whisper", t=1.0, db=-8), sfx("hit", src_t=684.1, db=-4), sfx("stinger", src_t=693.2, db=-2)]),
    blk([696.3, 707.6], "broll", max_pause=0.9, brolls=[c("wind", 10), c("lightning", 14), c("fog", 14)], light=0.9, dread=1,
        trans="flash", music_db=-15, amb_storm=-8, sfx=[sfx("gust", t=0.2, db=0), sfx("crack", t=2.0, db=-4), sfx("hit", src_t=706.2, db=-4)]),
    # ---------------- next day
    blk([710.1, 720.2], "broll", max_pause=0.9, brolls=[c("mistvillage", 2), c("mistvillage", 14), c("feet", 25)], light=0.45,
        dread=0.55, trans="fade", music_at=20, music_db=-19, amb_crickets=-36),
    blk([721.9, 729.8], "broll", max_pause=0.9, brolls=[c("scared", 2), c("scared2", 5)], light=0.6, dread=0.65, music_db=-18,
        sfx=[sfx("whisper", t=1.0, db=-10)]),
    blk([730.9, 742.4], "broll", max_pause=0.9, brolls=[c("incense", 3), c("incense2", 0), c("candle", 4), c("lanterns", 3)],
        light=0.6, dread=0.65, music_db=-18),
    blk([746.3, 761.1], max_pause=1.0, light=0.7, dread=0.75, zoom=[1.1, 1.25], music_db=-17, nosub=[[752.3, 758.4]]),
    blk([764.5, 773.0], "black", max_pause=1.0, light=1.0, dread=1, heartbeat=True, heartbeat_bpm=90, music_at=128, music_db=-14,
        cards=[card(764.6, [R("俺不是齊天大聖…")], 3.8), card(768.4, [W("俺不是他…")], 2.2), card(771.4, [R("不要…不要…")])],
        sfx=[sfx("whisper", t=0.2, db=-6), sfx("stinger", src_t=764.6, db=-3)]),
    blk([776.8, 795.2], max_pause=0.9, light=0.7, dread=0.7, zoom=[1.0, 1.1], trans="fade", music_db=-18,
        sfx=[sfx("hit", src_t=791.4, db=-10)]),
    # ---------------- moral
    blk([796.8, 815.0], max_pause=0.6, light=0.5, dread=0.5, zoom=[1.0, 1.06], music_at=40, music_db=-20),
    blk([816.0, 843.2], "broll", max_pause=0.7, brolls=[c("candle", 0), c("incense", 10), c("moonclouds", 18), c("fog", 15)],
        light=0.6, dread=0.6, music_db=-19, cards=[card(839.4, [W("你到底封了"), R("一個什麼東西？")])]),
    # ---------------- comic relief: lights back on
    blk([848.9, 884.9], max_pause=0.5, light=0.0, dread=0.05, zoom=[1.0, 1.05], trans="flicker", music_db=-30, amb_room=-32,
        sfx=[sfx("buzz", t=0, db=-12)]),
    blk([908.4, 938.2], max_pause=0.5, light=0.25, dread=0.3, zoom=[1.0, 1.08], music_at=30, music_db=-23),
    blk([[940.2, 950.6], [963.9, 969.4]], max_pause=0.4, light=0.0, dread=0.1, zoom=[1.0, 1.03], music_db=-26, amb_room=-32, fade_out=True),
]
edl = dict(audio=G + "/a48.wav", transcript=G + "/transcript.json", music=G + "/music/bgm48.wav",
           assets=dict(room=IMG + "10.webp", desk=IMG + "11.webp", sprites=SP + "/char"), fixes=fixes, blocks=blocks)
json.dump(edl, open(G + "/edl_full.json", "w"), ensure_ascii=False, indent=1)
print(len(blocks), "blocks")
