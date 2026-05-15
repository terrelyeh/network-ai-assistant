# RD Meeting Agenda · 推進 Troubleshoot Scripts (P0)

> 30 分鐘 · 你 + RD 主管 + 1-2 個會接手的工程師
> 目標：散會時拿到「X 月底前可以給你 5 個 op + method/path 標註」的口頭承諾

## Pre-read（24 小時前寄出）

寄出 3 個檔案 + 簡短信：

**信件草稿**：
> Subject: [Demo Unblocker] 5 個 troubleshoot ops + method/path 標註 — 求討論
>
> Hi [RD lead]，
>
> 為了 Network AI-Assistant 展會 demo，我們需要 5 個 troubleshoot op 被 callable（目前只有 references/*.md 沒 scripts/）。已驗證的 5 個 dashboard 都能跑了，缺這 5 個 op 才能解鎖最有戲劇張力的 demo 時刻。
>
> 附 3 個文件：
> 1. `02-ask-sheet.md` — 5 個 op 各自的 API spec proposal（你們照寫，不用猜需求）
> 2. `03-demo-storyboard.md` — 補完後解鎖什麼 demo
> 3. `architecture-demo.html` — 現況 5 個 dashboard 跑通的證明
>
> 想約 30 分鐘對齊範圍 + 時程。本週四 14:00 / 週五 10:30 兩個 slot 看你方便。
>
> Lulu

---

## Meeting 30 分鐘流程

### 0:00-0:03 · 開場 (3 min)

**你要說**：
> 「今天就 30 分鐘，目標很單純：把 5 個 troubleshoot op 的 scripts 補完，讓我們展會的 demo 從『audit / planning』升級到『即時操作』。先看 5 分鐘已經跑通的 demo，再進入具體 ask。」

**避免**：
- ❌ 「我們有一個很棒的計畫想跟你討論……」（虛）
- ❌ 「希望可以儘快……」（沒時間壓力）

### 0:03-0:10 · Live demo (7 min)

打開 `http://localhost:58778/architecture-demo.html`，按這個順序講：

| 時間 | 動作 | 你說 |
|---|---|---|
| 0:03 | 打開首頁 hero | 「整套架構 5 層，重點是這層——data skills 你們 13 個都做好了」 |
| 0:04 | 跳到 `#gallery` | 「我們已經組出 5 張 dashboard，全部用真實 staging API + 你們 13 個 skill」 |
| 0:06 | 點一張 dashboard demo（建議 S3 org-health） | 「對話 → 5 個 skill → 即時 dashboard。這就是 wedge 故事」 |
| 0:08 | 回到 `#limits` 區段 | 「**這是我今天來的原因**——你看這 3 個 🔴 區塊：troubleshoot 47 個 op 全部不能跑」 |
| 0:09 | 翻 `docs/rd-priorities.md` P0 section | 「不是要你補 47 個，只要 5 個最戲劇的就解鎖最多」 |

### 0:10-0:18 · 具體 ask (8 min)

打開 `02-ask-sheet.md`（投影 / 螢幕分享），逐項講：

| 時間 | Op | 你說 |
|---|---|---|
| 0:10 | **rpc_led_dance** | 「展會現場有 AP demo gear，AI 觸發 LED 閃，觀眾抬頭看到——**這 1 個 op 就值整個展會**」 |
| 0:12 | **rpc_kick_clients** | 「飯店 demo 場景：『7F 客人抱怨 wifi』→ AI 找出兇手 → 踢掉 → 立刻好了」 |
| 0:14 | **subscribe_client_list** | 「上面那個故事的前提——要先看到 client 才能踢」 |
| 0:15 | **subscribe_cable_diag** | 「Switch 線路斷在哪——對 IT manager 是 SOP 級需求」 |
| 0:16 | **rpc_reboot** | 「最 classic 的『AI 自療』橋段，補完 fleet 就完整」 |
| 0:17 | **method / path 補齊** | 「附帶請補一下，每個 op 在 SKILL.md 加 2 行就好，跟 `networks` skill 同格式」 |

### 0:18-0:25 · 對齊範圍 + 時程 (7 min)

**你主動問**（不是被動等他們講）：

1. 「這 5 個 op 你們估時多久？」
   - 預期回答：3-5 天 / 1 週 / 1 工作週
   - 如果說 > 2 週：問「是哪個 op 卡住？」（通常是 subscribe streaming）
2. 「能 commit 到 [展會日期] 前 2 週做完嗎？」
3. 「如果要砍項目你會先砍哪個？」（找出真正關鍵的 dependency）
4. 「Dolphin 平台支援的 timeline？」（CLAUDE.md 提過這個還在開發）

**如果他們推「太多了」**：
- ❌ 不要直接砍項目（你會吃虧）
- ✅ 反問「先補哪 3 個讓我先 demo？」
- ✅ 最差也要保住 `rpc_led_dance`（投資報酬率最高）

**如果他們問「為什麼這幾個」**：
- 拿出 `03-demo-storyboard.md`，每個 op 對應一個 demo 故事
- 強調「**我已經算過 ROI 了，不是隨便挑**」

### 0:25-0:28 · Q&A (3 min)

預期問題 + 你的回答：

| 問 | 答 |
|---|---|
| 「為什麼不等 Dolphin 整套？」 | 「Dolphin 是 2-3 個月後的事，展會這 2 個月需要 demo unblocker」 |
| 「subscribe 是 WebSocket 還是 SSE？」 | 「都行，看你們架構。SSE 對前端比較簡單」 |
| 「能不能我們先 mock 一個假版本給你？」 | 🟡「展會 demo 不能用 mock——觀眾資料人員會問『這真的是 live 嗎』。需要真實 API」 |
| 「能不能用 cloud GUI 截圖湊？」 | 🟡「那就完全沒 wedge 了，整套故事垮掉」 |
| 「展會什麼時候？」 | 給日期，並強調「需要展前 2 週測試」 |

### 0:28-0:30 · 收尾 (2 min)

**散會前要拿到的 3 件事**：

1. ✅ **明確的 owner**（不是「我們 team 處理」，是「[人名] 負責」）
2. ✅ **時程承諾**（不是「儘快」，是「[日期] 完成」）
3. ✅ **下次 check-in 時間**（建議 weekly Friday 15 分鐘）

**你結尾說**：
> 「謝謝，我會把今天的決議整理一份備忘錄寄給大家，包括 owner、時程、下次 check-in。**順帶一提，下個迭代我們要做趨勢類 dashboard，會需要 history aggregation API，下次跟你約一場專題討論**——今天先 focus 在 troubleshoot。」

→ **這句鋪梗很重要**，讓他們知道後面還有 P1 要談，這次不要塞太多就走。

---

## 散會後 1 小時內：寄備忘錄

```
Subject: [Memo] RD Meeting 結論 — 5 個 troubleshoot ops + method/path

Hi 所有人，

對齊結論：

| Item | Owner | Target Date | Notes |
|------|-------|-------------|-------|
| rpc_led_dance scripts | [Name] | [Date] | |
| rpc_kick_clients scripts | [Name] | [Date] | |
| subscribe_client_list scripts (SSE) | [Name] | [Date] | |
| subscribe_cable_diag scripts (SSE) | [Name] | [Date] | |
| rpc_reboot scripts | [Name] | [Date] | |
| method/path 標註 3 個 SKILL.md | [Name] | [Date] | |

Next check-in: 每週五 15:00, 15 mins

下次討論議題（待約）: history aggregation API (P1)

Lulu
```

---

## 失敗情境 & 備案

| 情境 | 備案 |
|---|---|
| RD 主管根本沒空 30 分鐘 | 改寄 5 分鐘 Loom 影片講同樣內容 |
| 工程師說「沒人會 WebSocket」 | 退讓到 SSE（比較簡單）；最壞 long-poll |
| 估時 3 週以上 | 砍到只要 3 個 op（保 led_dance + kick_clients + subscribe_client_list） |
| 完全沒人 own | 升級到請主管直接指派；如果不行，書面記錄「展會 demo 將 fallback 到冷凍版」 |
