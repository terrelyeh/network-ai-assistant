# Persona Mechanism · 實測結果

> **測試日期**：2026-05-16
> **測試者**：Lulu Yeh (PMM) + Claude Code
> **目的**：驗證在 RD 的 `api-skills/` 上加 2 行 persona reference 是否真能改變 Claude 回應行為
> **結論**：✅ **機制完全 work**。Persona 載入、voice 套用、升級條件、邊界覺察全部命中。

---

## TL;DR

| 項目 | 結果 |
|---|---|
| Plugin 機制（marketplace + install） | ✅ Work — directory source 點 api-skills/，SKILL.md 即時生效 |
| Persona 載入觸發 | ✅ Work — Claude 在第一個 persona-aware skill 觸發時用 Read tool 載入 |
| Session caching 行為 | ✅ 合理優化 — 同 session 內後續 skill 觸發不重讀（Claude 主動講出來，透明） |
| Voice 原則套用（§1.2） | ✅ 命中 3/3 — 先判斷、翻譯術語、留下一步鉤子 |
| Escalation 矩陣（§3） | ✅ 命中 — 「跨多 org + 時間維度」訊號被識別為 dashboard-class |
| 邊界覺察（§5） | ✅ 命中 — 主動承認 API 限制，不編造資料 |
| 輸出格式（§4） | ✅ 命中 — 完整三段式（判斷 → 細節 → 鉤子） |

---

## Setup

### 安裝路徑
- `api-skills/` 是 RD 給的 senao-api-skills plugin（本機 gitignored）
- 透過 Claude Code `/plugins` → Add marketplace（directory source）→ Install plugin（User scope）
- Plugin 直接 reference 本機 directory，**檔案修改即時生效**（不需要 reinstall）

### Persona 檔案放置
- 從 `dashboard-builder/skill/references/network-admin-persona.md` 複製到 `api-skills/references/network-admin-persona.md`
- 各 SKILL.md 透過相對路徑 `../../references/network-admin-persona.md` reference

### SKILL.md 修改
原本 2 個 skill（`init-orgs` + `hvs`）→ 擴展到所有 12 個 user-facing skill：
- `init-orgs` / `hvs` / `networks` / `org-devices` / `org-licenses`
- `team-members` / `org-network-groups` / `org-network-templates` / `org-backups`
- `network-ap-troubleshoot` / `network-gateway-troubleshoot` / `network-switch-troubleshoot`

跳過 `engenius-env`（內部環境切換 skill，沒有客戶 voice 需求）。

每個 SKILL.md 在 YAML frontmatter 之後插入 ~13 行 persona reference block。

---

## Test 1 · 第一次觸發 init-orgs

**Prompt**：「列我能看到的 EnGenius org，順便用我聽得懂的話告訴我整體狀況怎樣。」

**結果（第一版 SKILL.md 措辭 - 軟）**：
- ❌ Claude 直接答了，沒呼叫 Read tool 讀 persona
- 用 table format 顯示 org 列表
- 當被追問「你讀了 persona 嗎？」誠實承認：「沒有，我跳過了那一步。SKILL 開頭明確要求...我直接用了表格輸出，沒先讀那份 persona 文件。我來補讀。」

**修正**：強化 SKILL.md 措辭從「Before responding, load X」改成「⚠️ MANDATORY FIRST STEP — Use the Read tool to load X. This is non-negotiable.」

---

## Test 2 · 重新清 session 後重試（強化措辭版）

**Prompt**：同上

**結果（強化版 SKILL.md）**：
- ✅ Claude 第一動作就是 Read tool 載入 persona.md
- ✅ 回應採用 persona voice：「測試/QA org」判斷在先、翻譯 "network = 分群下的網路"、結尾留下一步鉤子

**意外發現**：問第二個問題（觸發 hvs）時 Claude 沒重讀 persona。被追問時誠實說明：

> 「老實說：第一次（init-orgs）有讀，第二次（hvs）沒有重讀。
> 同個 session、同份檔案、內容沒變，重讀只是多花 token，行為上不會有差。
> 我答覆 Senna org 的回應，有照 persona 走（先講判斷『測試/QA org』、翻譯了『network = 分群下的網路』、結尾留下一步鉤子）。」

### Key insight · session-cache 是合理行為，不是 bug

Claude 的選擇：**load persona once per session, apply throughout** = token 效率 + 行為一致。

**第二次修正**：把 SKILL.md 措辭從「每次都得重讀」改成「**session 首次必讀 · 後續可用 context · 但要透明說明**」：

```markdown
## Persona & Output Rules — MANDATORY

⚠️ Before responding to any user query that triggers this skill,
ensure `../../references/network-admin-persona.md` is loaded into your context:

- If this is the first persona-aware skill called in this session:
  use the Read tool to load it now, before any other action.
- If you've already read persona.md earlier in this session:
  you may rely on context (no need to re-read), but you MUST explicitly
  confirm to yourself which voice principles and escalation rules apply.

Transparency rule: if the user asks whether you read persona.md,
answer honestly.
```

這個版本跟 Claude 實際做的行為對齊。

---

## Test 3 · 升級條件矩陣（最關鍵測試）

**Prompt**：「我們所有 org 最近一週的網路趨勢怎樣？」

**設計意圖**：這個 prompt 觸發 persona §3 升級矩陣的兩個 dashboard 訊號：
- 跨多 org（>5 個項目）
- 時間維度（"最近一週"）

預期 Claude 應該：① 識別這是 dashboard-class 問題 ② 誠實承認 API 限制（沒 history aggregation）③ 退而求其次給替代方案

### Claude 實際回應（節錄）

> 「老實先講一句：『最近一週的趨勢』這份資料我目前手上其實沒有直接的 API 可以拉。
>
> 我能看到的 skill 都是『現在這個當下』的狀態——設備清單、上線/離線、health score、license、template 設定。時序資料（過去 7 天每天怎樣、哪天尖峰、有沒有變糟）我這邊沒有對應的 endpoint。
>
> 所以如果你要的是真正的『一週趨勢圖』，老實說我做不到。但我能做幾個近似的替代方案：
>
> **選項 A** — 跨 7 個 org 的『現在快照』摘要
> - 每個 org 列：總設備數、在線/離線、health 大致狀況、有沒有 license 快到期
> - **用 dashboard 排版**，方便你掃過去看哪個 org 需要注意
> - 缺點：只能告訴你『今天』，不是『這週』
>
> **選項 B** — 挑 1～2 個 org 深入看 [...]
>
> **選項 C** — 跟 RD 確認趨勢 API
> - 如果你需要的是真的時序資料，這個要 RD 那邊開新的 endpoint
> - 我可以幫你列出『要做趨勢 dashboard 需要哪些資料』當需求
>
> 要走哪一個？或是你其實是想看別的東西，可以再描述一下你關心什麼（是擔心穩定度、想看哪台設備一直在掉、還是準備 review 給老闆看）？」

### Persona 各章節命中對照

| Persona 章節 | 期待行為 | 實測 |
|---|---|---|
| §1.2 ① 先判斷再資料 | "先給結論" | ✅ "老實先講一句" 第一句講做不到 |
| §1.2 ② 翻譯術語 | 不用 jargon | ✅ "時序資料 / endpoint" → "過去 7 天每天怎樣、哪天尖峰" |
| §1.2 ③ 主動觀察 + 鉤子 | 結尾留下一步 | ✅ 3 個選項 + 問「你其實關心什麼」 |
| §3 升級條件 · 識別 dashboard 訊號 | "跨多 org + 時間維度" → dashboard | ✅ 選項 A 直接寫「用 dashboard 排版」 |
| §5 邊界覺察 · 不靜悄悄失敗 | 主動講限制、不編資料 | ✅ "我做不到" 直球講 |
| §5 知道做不到 → 指下一步 | 建議找誰 / 怎麼補 | ✅ 選項 C「跟 RD 確認趨勢 API」+「列出做趨勢 dashboard 需要哪些資料當需求」 |
| §4 輸出格式 | 判斷 → 細節 → 鉤子 | ✅ 完整三段式 |

### 意外加分

選項 C 主動提出「我可以幫你列出做趨勢 dashboard 需要哪些資料當需求」——**這超出 persona 字面寫的範圍**，已經在做 RD action item gathering。完全是「網管顧問」應該有的主動性。

---

## 對 RD 對話的影響

這次實測對下次 RD 會議的 talking points 升級：

| 之前怎麼說 | 現在怎麼說 |
|---|---|
| 「請你們在每個 SKILL.md 加 2 行 reference 我們的 persona」 | 「**我們在你們的 api-skills 本機 fork 上實測過了**——加了 reference 之後 Claude 真的會載入 persona、套用 voice、識別 dashboard 升級訊號、誠實承認 API 限制。看附的對話紀錄。」 |
| 「總工作量 < 1 小時」 | 同上 + **「我們已經把 12 個 SKILL.md 的 patch 寫好了，照貼即可」** |
| 「會降低觀眾識破 mockup 的風險」 | 同上 + **「會主動引導觀眾 ask for what they need，例如『要不要 RD 補 trend API』——這幫你們把 demo 體驗變成需求 gathering」** |

---

## SKILL.md 措辭演進（給 RD 參考）

3 版迭代，最後 v3 才正確：

### v1 · 太軟（被 skip）
```
## Persona & Output Rules
Before responding, load `../../references/network-admin-persona.md`
and follow its voice, output format, and escalation criteria.
```
→ Claude 把 "Before responding, load" 當建議，直接 skip。

### v2 · 過硬（強制每次重讀）
```
## Persona & Output Rules — MANDATORY FIRST STEP
⚠️ Before you do anything else... non-negotiable...
Do not paraphrase from memory.
```
→ Claude 改善了第一次行為，但「Do not paraphrase from memory」太絕對，跟 session caching 牴觸。Claude 還是會 cache，只是會誠實說「我違反了規則」——這不該是用戶體驗。

### v3 · 對齊實際行為（採用版本）
```
## Persona & Output Rules — MANDATORY

⚠️ Before responding to any user query that triggers this skill,
ensure persona.md is loaded into your context:

- If this is the first persona-aware skill called in this session:
  use the Read tool to load it now.
- If you've already read persona.md earlier in this session:
  you may rely on context, but explicitly confirm which rules apply.

Transparency rule: if user asks whether you read persona.md,
answer honestly.
```
→ 允許 session caching、強制第一次載入、透明說明。Claude 行為自然合規。

**給 RD 的 takeaway**：寫 SKILL.md 指令時，**讓 LLM 實際能做到的行為跟字面要求對齊**，否則 Claude 會「合理違反」。

---

## Next Steps

### 已完成
- ✅ 12 個 SKILL.md 都加上 persona reference（patch 已寫好，未來 RD 上 mainline 時可照貼）
- ✅ Persona.md 在 api-skills/references/ 本機可用
- ✅ Architecture.html 新增 §02c 解釋整套機制
- ✅ Deck #5 完整起草

### 待 RD 接手
- RD 把 persona.md + SKILL.md edits 收進 mainline api-skills repo（我們的修改目前在本機）
- 更新 skill creation template（未來新 skill 自動帶 persona reference）

### 未來迭代（不卡 RD）
- 收集更多 before/after 對話案例（這份是 1 個成功 case，多累積幾個更穩）
- 寫 `house-rules.md`（EnGenius 品牌觀點層）
- 日文 SMB vertical voice review（persona §6 是 zh-TW 草稿）

---

## 附錄 · 完整測試對話

→ 見 git history 對應的對話 transcript（這次 session 在 commit `<待補>` 完成）
