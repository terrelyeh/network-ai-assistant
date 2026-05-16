# Deck #5 · Persona 機制與 SKILL.md 修改提案

> 給：RD 主管 + 維護 `api-skills/` 的工程師
> 目的：用 < 1 小時的 RD 工作量，把所有 skill 升級成「有人格的 AI 網管」
> 估時：13 個 SKILL.md × 2 行 + 1 個 template 更新 = **< 1 小時**
> 不卡 P0 troubleshoot scripts、不卡 history API；可以併在下次 sprint 任何 PR 裡

---

## TL;DR

我們已經有 13 個 skill 跑通真實 staging API、5 個 dashboard validated。但 Claude 回答客戶問題時還是「裸 API 風格」— 看起來像 datasheet，不像「你的專屬網管」。

**提案**：
1. 我寫好一份 [`network-admin-persona.md`](../../skill/references/network-admin-persona.md)（356 行，已 commit）
2. RD 在每個 SKILL.md 最上面加 **2 行** reference 這份 persona
3. 之後所有 skill 觸發都會自動載入人格、輸出統一語氣

**效果**：同一個問題、同一份 API 資料，回應從「3 台 AP offline」變成「廚房那台 AP 從 14:23 開始失聯，可能是斷電，要我查嗎？」— 直接拉開 wedge 跟其他 AI 工具的差距。

> ✅ **2026-05-16 已實測通過** — 在 PMM 本機 fork 的 api-skills/ 上裝 plugin + 加 persona reference，Claude 真的會載入 persona、套用 voice、識別 dashboard 升級訊號、誠實承認 API 限制。**完整對話紀錄 + SKILL.md 措辭 3 版迭代教訓**見 [`persona-test-results.md`](../persona-test-results.md)。Deck 內所有 Before/After 範例現在都有實測背書，不只是假設。

---

## 1. 為什麼這個重要

### Wedge 故事的下一個 level

目前對外故事是「**AI 動態生 dashboard**」。
加上 persona 之後，故事升級成「**你的專屬 AI 網管 — 他會回答你、給建議、必要時開 dashboard 給你看**」。

| 沒 persona | 有 persona |
|---|---|
| AI = dashboard generator | AI = network admin（dashboard 是他的工具之一） |
| 一張圖就是答案 | 一段話 → 必要時開圖 → 必要時動手 |
| 跟其他「LLM + API」工具長一樣 | EnGenius 獨有體驗 |

對日本展會的價值：「Claude 自己判斷該開 dashboard 還是該講話」這個觀感，比「Claude 生 dashboard」更有 wow，且容易讓觀眾留下「這個 AI 真的懂網管」的印象。

### 對 SMB 客戶的價值

我們 ICP 是中小企業 — 餐廳老闆、診所經理、小學主任。他們**沒有專職 IT**。

「PoE budget 78%」對他們是亂碼。
「這台 switch 供電還有兩成餘裕，再插 1-2 台 AP 沒問題」是他能行動的答案。

Persona 內建了詞彙翻譯表 + 6 個 SMB vertical 適應（餐廳 / 零售 / 診所 / 學校 / 專業服務 / 設計），同一個 API 結果換不同 voice 講。

---

## 2. 提案的機制

### 三層分工

| 層 | 內容 | 誰寫 | 已備好？ |
|---|---|---|---|
| **persona.md** | Voice、輸出格式、升級條件（text / dashboard / action） | 我 | ✅ 已 commit |
| **SKILL.md reference 行** | 2 行指令告訴 Claude 「先讀 persona 再回應」 | RD | 🔜 這次 ask |
| **CLAUDE.md reference**（雙保險） | api-skills repo 工作目錄時 auto-load | RD | 🔜 順手加 |

### 為什麼需要每個 SKILL.md 加 2 行

**核心機制問題**：Claude Code 只在「skill 被觸發」的那一刻才會去讀那個 skill 的 SKILL.md。

如果 persona.md 不在 SKILL.md 裡被 reference 到 → Claude 永遠看不到它 → 整個機制等於沒裝。

唯一可靠的注入點就是 SKILL.md 本身。

---

## 3. 具體 RD ask

### A. 每個既有 skill 加 2 行（13 個 skill × 30 秒）

在每個 `SKILL.md` 最上面（YAML frontmatter 之後、第一個 section 之前）加：

```markdown
## Persona & Output Rules
Before responding, load `../../references/network-admin-persona.md`
and follow its voice, output format, and escalation criteria.
```

> **如果 `references/` 路徑跟你們現有結構不同，告訴我，我改 persona.md 的存放位置**。

### B. 把 persona.md 複製進 api-skills repo

```
api-skills/
└── references/
    └── network-admin-persona.md   ★ 從 dashboard-builder/skill/references/ 複製
```

我已經把它寫好放在 `dashboard-builder/skill/references/network-admin-persona.md`，
你們直接 `cp` 過去就好（檔案內容不需改）。

### C. 更新 skill creation template

如果有「新 skill 範本檔」，把上面那 2 行加進預設 template，
未來新 skill 自動帶這個 reference，不會漏。

### D. 在 api-skills/CLAUDE.md 也加一段（雙保險）

```markdown
## EnGenius Network Admin Persona
All skills in this repo share a unified persona defined in
`references/network-admin-persona.md`. Read it before invoking any skill.
```

> **D 是 bonus，B + A 才是 must-have**。

### 估時

| 項目 | 工作量 |
|---|---|
| A · 13 個 SKILL.md 各加 2 行 | 30 分鐘 |
| B · 複製 persona.md | 1 分鐘 |
| C · 更新 template | 10 分鐘 |
| D · CLAUDE.md 加 reference | 5 分鐘 |
| 1 人 review + merge | 10 分鐘 |
| **合計** | **< 1 小時** |

可以併在任何一個 P0 troubleshoot script PR 裡，不需要單獨排 sprint。

---

## 4. Before / After 對話範例（最關鍵的買單材料）

> 同一個 API 結果、同一個客戶問題。差別只在於 SKILL.md 是否載入了 persona。

### 範例 1：日常狀態問

**客戶**：「我們今天網路還好嗎？」（餐廳老闆，30 台 AP）

**Before（沒 persona）**：
```
組織目前有 30 個 device，狀態：online=28, offline=2。
Health score: 92/100。
Top alerts:
- 1F AP signal weak (-78 dBm, AP-LB-01)
- Switch port 14 link down (SW-01, port 14)
```
→ 客戶反應：「我是不是要報修？」（看不懂）

**After（有 persona）**：
> 「整體還好，30 台設備裡有 2 台需要注意。
> 一台是 1F 大廳的 AP 訊號偏弱（可能是新隔的 VIP 室擋到），另一個是後場 switch 第 14 號 port 沒在用、或線鬆了。
> 都不影響今天營業。要不要等收店後我幫你一起處理？」

→ 客戶反應：「好啊，那等等再說。」（理解、有掌控感）

### 範例 2：自動升級到 dashboard

**客戶**：「最近一週 Wi-Fi 表現怎樣？」

**Before**：
```
Last 7 days: 28 devices avg uptime 98.2%。
Peak channel util: Fri 19:00 (AP-LB-01: 87%, AP-LB-02: 82%, ...)
```

**After**：
> 「最近一週整體還好，但禮拜五晚上 19:00-21:00 有 4 台 AP 通道擠到爆 — 看起來是週末客滿 + 大家都用 Wi-Fi 訂位 app。
> 我拉一張趨勢 dashboard 給你看比較清楚，含每日尖峰時段、哪幾台 AP 受影響、建議怎麼調整。」
> *[Claude 自動觸發 compose.py → dashboard]*

→ 這就是 wedge 升級：**「AI 自己判斷該開 dashboard」**

### 範例 3：動手前的確認

**客戶**：「幫我把吧台那台 AP 重開」

**Before**：
```
Executing rpc_reboot for device 00:90:7f:06:61:14...
Done. Device rebooted.
```

**After**：
> 「我要重開『吧台-AP03』，大概 30 秒。
> 期間連那台的客人（看起來目前有 6 人）會斷一下，會自動跳到旁邊的 AP04。
> 要繼續嗎？」

→ 動手前確認 = 品牌安全立場（避免 AI 闖禍）

---

## 5. Token cost 評估

| 項目 | 估算 |
|---|---|
| persona.md 大小 | 356 行 / ~6 KB markdown / ~2,500 tokens |
| 每次 skill 觸發額外載入 | +2,500 tokens（context 預算內，可接受） |
| 對話成本增加 | 約 +5% per turn（Claude Sonnet 4.6 cache hit 後可忽略） |

**有 prompt cache 的話**：persona.md 第一次 hit 後就 cache 5 分鐘，同一場對話內後續 skill 觸發**幾乎 0 成本**。

**對展會 demo 的影響**：可忽略。每場對話約 5-10 turns，cache hit 後成本變化在 10% 內。

---

## 6. 預期 RD pushback + 回應

| 質疑 | 你的回答 |
|---|---|
| **「真的會 work 嗎？聽起來太抽象」** | **「實測過了，看 [`persona-test-results.md`](../persona-test-results.md)。在你們 api-skills 本機 fork 跑了 3 個測試 prompt，包含『跨多 org + 時間維度』升級條件測試，Claude 真的會主動建議『要不要 RD 補 history API』。」** |
| 「為什麼不直接寫進 system prompt？」 | 「Skill 是被 LLM 使用者載入的，我們控不到 system prompt。SKILL.md 是唯一可靠的注入點。」|
| 「Persona 太硬會限制 Claude 判斷？」 | 「Persona 只規範**怎麼講** + **什麼時候用什麼工具**，不規範**內容**。Claude 該講什麼自己判斷。」|
| 「356 行太長」 | 「Cached 之後成本可忽略。如果真要瘦身，§7 範例可以拿掉，剩 ~250 行。」|
| 「會 drift」 | 「§2 工具地圖那段可以 auto-generate（從 INDEX.md 同步）。其他段動得慢，每季 review 1 次即可。」|
| 「現在改要動到 13 個檔案，risky」 | 「就是加 2 行，不動程式邏輯。沒過測試最多影響 voice，不影響功能。」|
| 「Dolphin 之後會不會用不到？」 | 「Persona 是 LLM-agnostic 的內容守則，跟 Dolphin / Claude / 其他 LLM 無關。換 backbone 不用重寫。」|

### 容易誤踩的：不要把這個 ask 跟 P0 troubleshoot scripts 混在一起

P0 troubleshoot scripts 是「**做功能**」（解鎖 wedge demo）。
Persona 是「**改體驗**」（升級 voice / 升級 wedge 故事）。

兩者**獨立**，可以並行。RD 如果說「P0 還沒做完先別管 persona」，回應：

> 「Persona 不會 block P0 — 就 < 1 小時的工作，可以塞在任何 P0 PR 順手加。不做的話 P0 補完後 demo 體驗還是裸 API。」

---

## 7. Future scope（先別在這次 meeting 主推）

這次 meeting **只談 persona.md**。下面這層先鋪梗，不深談：

### 未來 P2 · house-rules.md（不在這次 ask）

是「EnGenius 品牌觀點」層 — Claude 無論如何也猜不到的東西：

- HVS 分數區間怎麼解讀（< 70 / 70-85 / 85+ 各代表什麼）
- 永遠不推薦的反 pattern（例：「測連線把 WPA2 關掉」）
- BASIC vs PRO 推薦原則
- 平台特有 gotcha（cloud show offline 但現場正常 → 多半是 cloud-agent 沒同步）

預估 100-150 行內，需要 RD + 業務 + PMM 共同定義「品牌觀點」，這次先不卡 RD。

### 未來 P2 · Help Center / Gitbook RAG 對接

你們已經有 `ingest-helpcenter` + `ingest-gitbook` skill。
未來可以讓 persona §2.4 加一條「需要詳細排查步驟 → 查 RAG」的觸發條件。

這需要 RAG endpoint 從 skill 內部 callable，是另一個 work item。

---

## 8. 下一步

| Step | Owner | When |
|---|---|---|
| 1. 你 read 完 persona.md | 你 | 會議前 24h |
| 2. 對「path 是 `references/` 還是別的位置」給 feedback | 你 | 會議當下 |
| 3. 派 1 個工程師接 13 個 SKILL.md edit | RD | 會議散會時 |
| 4. 一個 PR 包含 §3 A+B+C+D | RD | 1 週內 |
| 5. Merge 後我這邊跑驗證對話（before/after 比對） | 我 | PR merge 後當天 |
| 6. 把驗證結果寫成展會 talking point | 我 | 驗證後 1 天 |

---

## 9. 會議 talking points（5 分鐘版）

如果這次 meeting 真的塞滿 P0 troubleshoot 沒空談 persona，**塞進 P0 sprint 結尾的 5 分鐘**用這個版本：

> 「最後 5 分鐘想加一個小 ask — 1 小時內可以做完，不卡 P0。
>
> 我寫了一份 360 行的 `network-admin-persona.md`，目的是讓 13 個 skill 共用同一個『網管顧問』語氣 — 跟 SMB 客戶講話用『廚房那台 AP 失聯』而不是『AP-LB-01 offline』。
>
> 機制很簡單：persona.md 放進你們 references/，然後每個 SKILL.md 上面加 2 行 reference。
>
> 我把這份 ask 寫成 `05-persona-proposal.md`，會議結束後我會把 PR commit hash 寄給你。要不要在任何一個 P0 PR 順手加進去？」

---

## 10. 附錄 · persona.md 速查（給 RD 在會議中翻）

| § | 主題 | 行數 |
|---|---|---|
| TL;DR | 我是誰 | 5 |
| 1 | Identity & Voice（4 條原則 + 15 個詞彙翻譯） | 70 |
| 2 | Capability Map（4 大類工具 + Status badge） | 45 |
| 3 | 升級條件矩陣（text / dashboard / action） ⭐ | 30 |
| 4 | 輸出格式（3 種模板） | 50 |
| 5 | 邊界與升級（不做的事、Plan/RBAC 自覺） | 35 |
| 6 | SMB Vertical 適應（6 個產業） | 30 |
| 7 | 對話範例（good vs bad） | 50 |
| 8 | 給 LLM 的執行指示 | 15 |
| 9 | 維護注意事項 | 12 |

完整檔案：[`dashboard-builder/skill/references/network-admin-persona.md`](../../skill/references/network-admin-persona.md)
