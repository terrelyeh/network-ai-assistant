# Booth Presenter Cheat Sheet · Hospitality Demo

> **印出來折半放口袋**。展會操作員用。
> 對應頁面：`prototype/booth-hospitality.html`
> 版本：v1 · 2026-05-13

---

## 鍵盤操作（投影機接你電腦那台）

| 鍵 | 動作 |
|---|---|
| `SPACE` 或 `→` | 下一個 phase |
| `←` | 上一個 phase |
| `R` | Reset 回 Phase 0（換訪客時按） |
| `1` `2` `3` `4` `5` | 直接跳到 phase N |
| `H` | 隱藏 / 顯示底部 hint bar |

5 個 phase 對應的時間 / 訊息：

```
P0 ATTRACT        待機/招攬          無時限 — 等訪客停下
P1 QUESTION       問題打字           ~3 秒 typing
P2 AI THINKING    5 個 tool call     ~7 秒
P3 DASHBOARD      4 widgets 浮現     ~2 秒 reveal + 觀眾看 60-90 秒
P4 COMPARE        舊 vs 新對比        最後 wow + 收尾
```

---

## 訪客類型 → 對應 talking script

### 「我做飯店 IT」（最佳契合）
```
P0 → [訪客停下] →
"hey 你是飯店 IT？我們有個 demo 你會喜歡 — Press SPACE"
P1 →
"假設你是飯店 IT 主管。客人抱怨 Wi-Fi 慢，傳統 dashboard 你要切 5 個畫面。
 看 AI 怎麼一句話解決："
[螢幕：客房 Wi-Fi 哪幾層樓在出問題？]
P2 → [SPACE]
"AI 在挑工具、呼叫真實的 EnGenius Cloud API ——"
[5 個 tool call 跑]
P3 → [SPACE]
"dashboard 30 秒生好。重點 ↓"
[手指 3F red row] "3F 過載"
[手指 5F red row] "5F 訊號弱"
[手指右側 AI 卡] "AI 直接告訴你誰是元兇 + ROI 估算"
P4 → [SPACE]
"這個 demo 不是要取代你們現用的 dashboard ——
 是補上『你特定想看的角度』，30 秒生，不用排開發。"
[要名片 / 留 contact]
```

**講話節奏要點**：
- 不要急著按下一個 phase — 每個 phase 給觀眾 5-10 秒消化
- 手要指著螢幕上具體元素（floor / AP name / AI card）
- 數字念出來（「3F · 47 個 client · 紅色」）— 觀眾沒在仔細看

---

### 「我在零售連鎖 / 學校 / 工廠」（不同產業 → 切換版本）

**目前只做 Hospitality**。其他 vertical 還在開發中。

應對：
```
"哇我們也有零售業的版本但今天 demo 是飯店 — 概念一樣，
 換成『哪家分店今天客流多少 / license 快過期』。要看的話留 contact 我傳給你。"
```

**絕不要硬切到「飯店 demo 解釋給零售業」**——故事會斷。

---

### 「不太懂技術，可以給我看一下嗎」

```
P0 → "好啊看吧" → SPACE
P1, P2, P3 一路按到底（不要在 P2 多解釋）
P3 重點停留 → "你看，AI 直接幫你找到問題在 3F"
P4 → "差別在這 — 以前你要等 IT 排，現在 30 秒"
```

技術細節跳過。重點是「快」+「自動找問題」。

---

### 「這真的能跑？資料是真的嗎？」（技術型訪客）

```
P3 dashboard 出來後 →
"這個 demo 是預錄的，但底下的 API skill 是真的 —
 我們有另一個 PoC 連 staging 真 API → [打開 dashboard-live.html] →
 看，這 5 個 org / 14 個 network 都是真的從 falcon.staging 抓回來的。"
```

→ 預錄 + 真 PoC 兩個都有，看訪客需求切。

---

## 救命 5 條（出意外時）

1. **投影機掛了 / 訊號斷了** → 把筆電轉向訪客，「直接看我這邊」
2. **PoC 連 staging 連不上**（如果有人要看真版）→ 只用 booth-hospitality.html（不需要網路）
3. **訪客問深技術** → 「這個我們 RD 比較適合聊，我們 booth 號 XXX 或留 contact」
4. **訪客挑刺說「AI 會幻覺」** → 「對，所以我們設計成 closed widget catalog — AI 只能挑 12 個 widget，不能瞎生 — 有限制反而穩」
5. **連續來訪沒空換訪客** → 按 R 重置，假裝沒事直接 P0 重來

---

## Demo 結束 close 的 3 種版本

### 30 秒收尾（隨意路人）
> 「謝謝看 demo！這是 QR code（指 booth 桌上）掃了會看到 6 個 vertical 的範例頁。」

### 1 分鐘收尾（有興趣的）
> 「對你們業務有幫助嗎？我可以記一下 contact，下週寄完整 demo 影片給你，看你想看哪個 vertical 細節。」

### 5 分鐘收尾（合格 prospect）
> 「想實際 hands-on 嗎？我可以排一個 30 分鐘 1-on-1 給你看 staging 跑真實 API 的版本，連你們的部分 use case 一起跑。」
> [拿名片 / 加 LINE / 排會議]

---

## 同仁準備清單（上場前 1 小時）

- [ ] 筆電充電到 100% + 帶充電器
- [ ] 投影機接線測試（HDMI / Mini DP / Type-C 帶齊）
- [ ] 螢幕解析度設成 1920×1080
- [ ] 瀏覽器：開 booth-hospitality.html，按 F11 全螢幕
- [ ] 備用：開另一分頁 dashboard-live.html（給技術型訪客）
- [ ] 桌上放：QR code（指向 home-product.html）+ 名片
- [ ] 確認筆電不會 sleep（System Preferences → Energy）
- [ ] 把 hint bar 留著（按 H 可隱藏）— 讓觀眾知道 SPACE 可按
- [ ] 練習 3 次完整 demo，每次 90 秒內跑完 P0→P4

---

## 常見問題 + 回答

| Q | A（30 秒內回完） |
|---|---|
| 這 dashboard 是哪邊抓的資料？ | 「demo 是預錄 hospitality 樣本資料。但底下的 API skill 都是真的，已經跟我們 staging 環境跑通了，可以 demo 連真實 API 的 PoC 給你看。」 |
| AI 會不會亂生？ | 「不會。AI 只能從 12 個 widget 裡挑（closed catalog），每筆 API 回應都過 Zod 驗證才能 render。」 |
| 多少錢？ | 「pricing 還在規劃中，但定位是 SMB IT 升級 / vertical 解決方案的 add-on。你留 contact 我寄 pricing intro 給你。」 |
| 跟既有 EnGenius 平台關係？ | 「擴充，不取代。底下用同一套 API、同一套 device 管理 — AI 只是讓你『用講的』組 dashboard。」 |
| 什麼時候上市？ | 「PoC 已經跑通，預計 6-8 週內展示 design partner 試用版。對加入 design partner 有興趣嗎？」 |
| 跟 Cisco Meraki / Aruba AI 比？ | 「他們是『AI 幫你 troubleshoot』，我們是『AI 幫你組 dashboard 看你想看的角度』— 不一樣的 wedge。詳細的我可以給你完整 positioning doc。」 |
| 支援 Dolphin 嗎？ | 「Falcon 平台先支援，Dolphin 正在開發中。」 |

---

## 緊急聯絡

- **PoC 在 GitHub**: github.com/terrelyeh/network-ai-assistant
- **Live PoC URL**: https://network-ai-assistant.vercel.app
- **API spec**: s3-us-west-2.amazonaws.com/liveapi-console-dev/engenius/falcon/index.html
- **若 booth 出大事 → 找** [PM 主管 / 你的聯絡人]

---

## 改進回饋

展會結束記得收：
- 哪幾段觀眾笑了 / 點頭
- 哪個 phase 失去注意力
- 訪客自己出的問題（→ 加入下次的 scenario 庫）
- 哪個 vertical 最多人問（→ 下次補 demo 優先序）
