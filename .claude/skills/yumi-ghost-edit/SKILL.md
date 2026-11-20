---
name: yumi-ghost-edit
description: 剪「玉米講鬼 TALK」鬼故事影片（16:9 長片）。輸入一段玉米的鬼故事音檔，剪掉廢話與空白、重排成越講越恐怖的結構，玉米在直播間對嘴主持，逐句配 B-roll、破碎字卡、繁體字幕、恐怖配樂與音效。使用者說「剪玉米講鬼」「把這段鬼故事剪成影片」「用玉米的風格剪」時使用。
---

# 玉米講鬼 剪輯 skill

把一段「只有聲音」的鬼故事，剪成玉米當主持人、會越看越毛的 16:9 影片。
第一集《黃皮子討封》(2026-11) 的完整工程檔在 `episodes/黃皮子討封/`，有問題先照那集抄。

## 0. 環境準備（每個新的雲端環境做一次）
```bash
apt-get install -y fonts-noto-cjk fonts-noto-cjk-extra        # 繁體字幕/字卡字型
pip install opencv-python-headless scipy pypinyin faster-whisper fonttools brotli
```
- ffmpeg 需要有 libass / loudnorm（Ubuntu 套件版即可）。
- 網路要放行：`drive.usercontent.google.com`、`drive.google.com`（從 Drive 下載素材）、`videos.pexels.com`（圖庫 B-roll）。
- 語音辨識模型：faster-whisper `small` 的 CTranslate2 權重放在 `/tmp/wm/model`。Hugging Face 的檔案 CDN 若被擋，第一集是從 npm 套件 `@skillninja/shortmovie-telop-model-p0..p3` 拼回來的（權重檔，非程式碼；與官方 checksum 不同，辨識結果一定要人工校對）。

## 1. 素材
| 東西 | 位置 | 說明 |
|---|---|---|
| 玉米嘴型 | `assets/mascot/v_*.png` | closed/half/open/wide/o/frown/blink，512px。新造型用 `tools/make_mouth_sprites.py` 從 3×2 表情表產生 |
| 直播間 | `assets/studio/room.webp`、`desk.webp` | 背景 + 透明桌面前景層（麥克風在左） |
| 配樂 | `assets/music/horror_bgm.mp3` | vidIQ AI 生成的中式民俗恐怖配樂（免版稅）。0–70s 鋪陳、75s 起爬升、120–145s 最緊張 |
| 字型 | `fonts/` + 系統 Noto CJK | 字幕＝Noto Sans CJK TC Black；字卡/標題＝Noto Serif CJK TC Black 加破碎效果 |
| B-roll / 音效 | **不放 repo**，放使用者 Google Drive | 圖庫授權不可再散布；Pexels 需署名 |

**B-roll 來源優先順序**：使用者用 Gemini（Veo）生成的故事專屬鏡頭 > Vecteezy（使用者帳號）> Pexels（vidIQ `vidiq_find_broll`）。
需要使用者動手時，產生「給本機 Claude 的指令」讓他貼到本機 Claude in Chrome 執行（範本見 episode 資料夾的兩個 .md）。
本 skill 不可替使用者登入網站或繞過網站的防機器人驗證。

## 2. 流程
1. **下載音檔**（Drive → `a48.wav` 48k mono；`a16.wav` 16k 給辨識）。量 LUFS，原片常在 −19，成片目標 −14。
2. **逐字稿**：faster-whisper word timestamps → `transcript.json`。
3. **讀完整份逐字稿再決定剪法**（不要只看開頭）：
   - 冷開場：把高潮裡「鬼的台詞」2–3 句提前當鉤子（~15s）→ 標題砸下。
   - 玉米開場只留打招呼 + 一句話講完傳說 + 「亂回答會怎樣」這類鉤子；**故事要在 1 分鐘內開始**（使用者明確要求：前面介紹不能長）。
   - 刪：更新時間/閒聊、重複的背景解說、「我怎麼找到這故事」。
   - 故事本體幾乎全留；結尾的笑點保留當鬆一口氣，再收結論、訂閱、拜拜。
   - 聽不清楚的句子不要亂猜；改用「停頓 + 燭火 + 心跳」接過去（第一集廟祝段落的做法）。
4. **寫 EDL**（`build_full_edl.py` 範本）：每個 block = 一段旁白 + 模式（host/broll/black）+ `light`（0 暖 → 1 全黑）+ `dread`（配樂/環境音強度）+ 字卡 + 音效。`max_pause` 越恐怖留越長（0.35 → 1.3s）。
5. **字幕**：用剪好的旁白重新辨識一次（時間軸才會對齊成片），再**逐句人工校對成繁體**（`subs_v2.py` 範本，`|` 是斷行點，`None` = 故意不上字幕）。常見錯字見 EDL 的 `fixes`（英國→因果、秘密→玉米、黃蜀狼→黃鼠狼、討風→討封…）。
6. **逐句分鏡**（`shots_v3.py` 範本）：`[成片秒數, None, 素材名 | "host"]`。規則：
   - 每句畫面要對到台詞內容；**對不上就回玉米主持畫面，不要硬塞**（使用者明確要求）。
   - 單一畫面最長 3 秒（引擎自動切）。
   - 引擎的 no-repeat planner 保證同一段素材只用一次；用完先鏡像+推近，再不夠就回 host。完全相同的檔案要先合併成同一個名字（`cmp` 檢查）。
7. **算圖**：
   ```bash
   python3 -I engine/ghost.py edl.json out.mp4 --video-only --stills 30,120,250   # 先抽幾張圖檢查
   python3 -I engine/ghost_parallel.py edl.json final.mp4 4                       # 4 段平行（7.5 分鐘片約 25 分鐘）
   python3 -I engine/ghost_parallel.py edl.json final.mp4 4 --reuse-video        # 只換音效/混音時，約 3 分鐘
   ```
   預覽版：`ffmpeg -i final.mp4 -c:v libx264 -b:v 3000k -c:a copy preview.mp4`。
8. **交付前檢查**：抽 6–10 張圖；量 LUFS（−14 ±0.5，TP ≤ −1.5）；字卡/字幕是否被 duplicated 原文時間誤對（引擎已改成 block 內對時）。

## 3. 風格規格
- **畫面**：16:9 1920×1080 30fps。直播間：房間背景微模糊、玉米 1.2× 坐在桌後、桌子前景層；左上「玉米講鬼 TALK／民間怪談系列」標籤。
- **燈光隨恐怖程度**：`light` 0→1，房間變暗、去飽和、偏冷、加暗角；B-roll 統一冷色去飽和 + 膠片顆粒；`red` 素材加紅。
- **玉米**：中文拼音韻母決定嘴型（a 類大張、o/u 圓嘴、e/i 半張、b/p/m 先閉），靜音自動閉嘴，2–5 秒隨機眨眼，呼吸起伏。`light ≥ 0.55` 時閉嘴改用皺眉臉。B-roll 時縮進右下紅框圓形小窗繼續對嘴。
- **字卡**：鬼/怪物的台詞用破碎宋體，白字 + 血紅字（`#E82226` 帶紅光），出現時閃爍；host 畫面時放左側避開玉米的臉。
- **標題**：白字＋血紅副標＋做舊金色紙條，砸下時震動＋重擊。
- **字幕**：底部置中、白字黑邊、每句 ≤14 字，**永遠顯示**（字卡出現時也要顯示）。
- **轉場**：硬切為主；換場 fade；燈閃 flicker；狂風 flash。
- **聲音**：人聲高通+壓縮 → 配樂（鋪陳段用前段、恐怖段跳到爬升段，講話時自動壓低）→ 環境音床（蟲鳴/風/暴風/室內）→ 心跳（恐怖段）→ 一次性音效（低語、貓頭鷹、腳步、草叢、樹枝斷、重擊、吸氣聲、廟鐘、木魚）。最後兩段式 loudnorm −14 LUFS。真實音效檔透過 EDL 的 `sfx_files` / `bed_files` / `heartbeat_file` 指定，缺的會用 `engine/foley.py` 合成版。
- **節奏參考**：16 分鐘原音檔 → 約 7.5 分鐘成片；冷開場 0:00、玉米開場 0:12、故事 0:58、高潮 ~2:40。

## 4. 已知限制
- 語音辨識錯字多（尤其馬來西亞口音、後段會跑成簡體），字幕必須人工校對。
- 玉米素材只有 512px，主持畫面放大後偏軟；有高解析度原圖要換掉 `assets/mascot`。
- 「狂風大作」那一下陣風仍是合成音效。
- EDL 範本裡的路徑是第一集當時的暫存路徑，換環境要改成新的位置。
