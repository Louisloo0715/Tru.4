請用 Claude in Chrome 幫我在 Gemini（gemini.google.com）生成影片素材，給 YouTube 頻道「玉米講鬼」的《黃皮子討封》這集使用。總共 17 支，分成 A、B 兩部分。請按照「優先順序」欄的數字從 1 開始做，額度用完就停下來告訴我做到哪裡（不要付費），明天再繼續。

---
## A 部分：同一個男人（11 支）—— 一定要用參考圖
故事裡的男人是同一個人，每支都要看起來是同一張臉、同一套衣服。

**參考圖**：先到 Google Drive 素材資料夾下載 `REF_村民男子.png`
https://drive.google.com/drive/folders/1Yygqq_8nH5n-5gvgFO87BpreLG0Xiw27
（一位拿著酒瓶、頭髮灰白凌亂、鬍渣、穿舊中式棉襖的中年村民）

**每支都做兩步：**
1. **先做圖片**：在 Gemini 開新對話，上傳 REF_村民男子.png，貼上：
   > Use the man in this photo as the character reference. Keep his face, age, messy greying hair, stubble and clothes (worn dark padded Chinese jacket with frog buttons over a patched grey shirt) exactly the same. Create a 16:9 cinematic photorealistic image: 【場景】. Dark night, cold blue moonlight, thin fog, rural Chinese mountain setting. No text.

   檢查：臉和衣服要明顯是同一個人，不像就重做一次。下載圖片，檔名＝表格「檔名」＋`.png`。
2. **再做影片**：用 Gemini 的影片生成（Veo），上傳剛剛那張圖片當起始畫面，貼上：
   > Animate this image: 【動作】. Slow subtle camera movement, keep the man's face and clothes unchanged, 16:9, no text, no subtitles.

   下載影片，檔名＝表格「檔名」＋`.mp4`。

**影片額度用完時**：只做步驟 1 的圖片，把 .png 上傳也可以（剪輯那邊會把圖片做成動態畫面）。

| 優先順序 | 檔名 | 場景（步驟 1） | 動作（步驟 2） |
|---|---|---|---|
| 1 | M03_crouch_tease | the same man crouching on a dirt mountain road at night, grinning mischievously down at a small yellow weasel standing upright in front of him | he leans in and teases the weasel, grinning |
| 2 | M06_frozen_fear | the same man standing on a night mountain road, suddenly frozen with terror, eyes wide | he trembles, breath visible in the cold air, unable to move |
| 3 | M10_temple_eyes | the same man inside a candlelit Taoist temple, incense smoke, looking up | his eyes slowly turn cold and an unsettling smile spreads across his face |
| 4 | M08_dazed_dawn | at misty dawn, the same man sitting on the ground at the foot of a mountain, dazed, staring at nothing, clothes dirty | villagers' lanterns slowly approach in the background; he does not react |
| 5 | M09_muttering | close-up of the same man in a dim old village house, vacant eyes, sweat on his forehead | his lips move as he mutters to himself |
| 8 | M01_walk_back | the same man seen from behind, walking alone along a narrow dirt mountain path at night, holding a green glass bottle | he walks away from the camera, swaying slightly |
| 9 | M05_laugh | the same man on the mountain road throwing his head back laughing loudly, bottle in hand | he laughs, then looks down at something on the road |
| 10 | M04_grin | close-up of the same man smirking, eyes narrowing with mischief | he chuckles to himself |
| 11 | M07_legs_stuck | low angle on the same man's worn black cloth shoes on a dirt road at night | he tries to step away but his feet won't lift off the ground |
| 12 | M11_carried_home | at dawn, two villagers in old work clothes supporting the same man under his arms, walking him back along a village path | they walk slowly toward the camera, his head hanging |
| 13 | M02_walk_side | the same man walking along a dirt mountain path at night, side view, bottle in hand | tracking shot following him as he walks, slightly unsteady |

---
## B 部分：場景與效果（6 支）—— 不需要參考圖
直接用 Gemini 的影片生成。每支的提示詞＝表格「提示詞」＋這段統一風格：
> Cinematic, photorealistic, dark night, cold blue moonlight, thin fog, rural Chinese mountain area, slow subtle camera movement, 16:9, no text, no subtitles, no modern objects.

| 優先順序 | 檔名 | 提示詞 |
|---|---|---|
| 6 | E03_storm_trees | Violent wind suddenly tearing through bare trees on a mountainside at night, branches thrashing, dead leaves flying |
| 7 | G15_shadow_monkey | The shadow of a weasel on an old stone wall lit by a single candle slowly morphs into the shadow of a man holding a long staff, the candle flickers |
| 14 | E02_dirt_road_night | An empty narrow dirt road winding through a mountain forest at night, no lights at all, only moonlight on the path |
| 15 | E04_lightning_mountains | Lightning flashes over dark mountain ridges and bare trees at night, illuminating swirling fog |
| 16 | E05_temple_exterior | Exterior of a small old Taoist temple in a mountain village at dawn, red lanterns, incense smoke drifting from the doorway |
| 17 | E01_village_night | Establishing shot of an old Chinese mountain village at night, tiled roofs, a few dim lantern lights, fog in the valley |

---
## 上傳
1. 把做好的 .mp4（和只做了圖片的 .png）全部上傳到：
   https://drive.google.com/drive/folders/1Yygqq_8nH5n-5gvgFO87BpreLG0Xiw27
2. 檔名一定要照表格改好（例如 `M03_crouch_tease.mp4`），剪輯那邊會自動對到正確的句子。
3. 最後列出：哪些做了影片、哪些只有圖片、哪些還沒做。
