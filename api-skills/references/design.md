# Dashboard Design Rules · EnGenius Network AI-Assistant

> **Version**: v0.2 (2026-05-17)
> **Audience**: Claude / any LLM agent composing dashboards via `dashboard-builder` skill
> **Goal**: 讓 AI 在 widget library 之外保留自由度，**同時**確保每張 dashboard 看起來像同一個產品

> ⚠️ **使用情境注意**：本文件假設 dashboard 用在 **demo 帳號 / 開發者自己的 staging 帳號**。如果是 SI / Partner 用自家帳號**幫終端客戶**跑生產 dashboard，請手動加上 PII 匿名化處理（員工姓名、email 等）— 這個 case design.md 不規範，由 SI 自己判斷情境。

---

## TL;DR

每張 dashboard 都長三層：

```
┌─────────────────────────────────────────────┐
│ Layer 1 · Frame（強制 · compose.py 自動套）   │
│  Logo · Refresh · Live · Footer · Auto-poll │
├─────────────────────────────────────────────┤
│ Layer 2 · Design tokens（強制）              │
│  CSS variables for color / type / spacing   │
├─────────────────────────────────────────────┤
│ Layer 3 · Body content（自由）               │
│  Widgets OR raw_html, AI choose             │
└─────────────────────────────────────────────┘
```

**規矩**：Layer 1+2 不可違反，Layer 3 自由發揮 — 但要套 tokens、要在無法用 widget 時於 raw_html section 內留 comment 說明「為什麼這裡要 hand-roll」。

---

## 🚫 絕對不能做（Hard Prohibitions）

**下面 9 條沒有例外**。違反任一條 → 停下、詢問使用者、不要 generate。這些是「會破壞 demo / 違法 / 系統會崩」的紅線。

| # | 類別 | NEVER | 理由 |
|---|---|---|---|
| ① | 安全 | 在 raw_html 或任何輸出中放 API key / token / password / secret | 即使 demo 也會在 screenshot / git history 留痕，外洩風險 |
| ② | 安全 | 在 raw_html 內 `fetch()` 外部 URL（compose.py 已 inject Google Fonts 是唯一例外）| 資料不應該離開 dashboard 上下文 |
| ③ | 安全 | 用 `eval` / `new Function(...)` / `setTimeout("string", ...)` | 代碼注入路徑 |
| ④ | 系統 | 在 raw_html 內寫 `<script>` 標籤 | runtime.js 是唯一執行環境，外部 script 繞過 widget event bus |
| ⑤ | 系統 | 引外部 JS / CSS lib（Chart.js / D3 / Bootstrap / FontAwesome / Tailwind CDN）| 視覺一致性 + i18n + theme switch 全崩 |
| ⑥ | 系統 | 用 `!important` 蓋 theme tokens | 破壞 dark mode cascade |
| ⑦ | 品牌 | 連結到競品（Cisco / Aruba / Ubiquiti / Meraki / TP-Link / Netgear 等）| 不要在自家 dashboard 幫客戶看到競品 |
| ⑧ | 品牌 / 法務 | 編造不存在的功能（「點此續訂」「升級 PRO」按鈕沒後端支援，按了沒反應）| 信任受損 + 可能涉及不實宣傳 |
| ⑨ | 品質 | 用棄用 HTML（`<marquee>` / `<blink>` / `<font>` / `<center>` / `<frameset>`）| 1990 年代的東西，現代瀏覽器不一定 work |

> 軟性的「不建議但不會崩」反 pattern → 見 §8 Soft anti-patterns。差別：§🚫 是「**遇到就停**」，§8 是「**儘量避免**」。

---

## 1. Frame · 強制套用，不要重寫

`compose.py` 自動把以下元素包進每張 dashboard，你**不需要** 在 spec 裡指定，**也不要** 自己寫 `<html><head>`：

| 元素 | 位置 | 來源 |
|---|---|---|
| EnGenius logo | 左上 | `assets/engenius-logo.png` |
| 標題 + 副標題 | logo 右側 | `spec.title` + `spec.subtitle` |
| Refresh 按鈕 | 右上 | compose.py 內建 |
| Live indicator（綠點 pulse） | 右上 | compose.py 內建 |
| Updated timestamp | 右上 | runtime.js |
| Sticky header bar | 整個頁面頂端 | base.css `.db-hdr` |
| Footer attribution | 頁底 | `spec.footer.ops_used` |
| 5 秒 auto-poll | 全頁 | runtime.js |
| 字體（Inter / Noto Sans TC / JetBrains Mono） | 全頁 | Google Fonts CDN |

⚠️ 不要在 raw_html section 裡重寫 header、footer、`<title>`、`<meta>`、Google Fonts link — 這些都已經有了。

---

## 2. Design tokens · 強制用 var(...)，不要 hardcode

### 2.1 顏色

| Token | 用途 | Light 值 | Dark 值（自動 cascade）|
|---|---|---|---|
| `var(--bg)` | 整頁背景 | `#fbf8f1` (warm cream) | `#0f172a` |
| `var(--surface)` | 卡片底色 | `#ffffff` | `#1e293b` |
| `var(--surface-2)` | hover / 次階卡片 | `#fbf9f3` | `#334155` |
| `var(--border)` | 一般邊線 | `rgba(60,50,35,.10)` | `rgba(255,255,255,.12)` |
| `var(--border-strong)` | 強邊線 | `rgba(60,50,35,.20)` | `rgba(255,255,255,.24)` |
| `var(--text-1)` | 主文 | `#1a2332` | `#f1f5f9` |
| `var(--text-2)` | 次文 | `#4a5568` | `#cbd5e1` |
| `var(--text-3)` | 說明 / meta | `#8b95a4` | `#94a3b8` |
| `var(--brand)` | 互動 / accent | `#ff6b35` (橘) | 同 |
| `var(--success)` / `--success-bg` | 良好狀態 | `#047857` / `#ecfdf5` | 自動切換 |
| `var(--warning)` / `--warning-bg` | 注意狀態 | `#b45309` / `#fffbeb` | 自動切換 |
| `var(--critical)` / `--critical-bg` | 嚴重狀態 | `#b91c1c` / `#fef2f2` | 自動切換 |
| `var(--info)` / `--info-bg` | 資訊狀態 | `#1d4ed8` / `#eff6ff` | 自動切換 |

❌ 不要寫 `color: #047857`
✅ 要寫 `color: var(--success)`

### 2.2 字體 / 字距

| Token | 用途 |
|---|---|
| `var(--font-sans)` | 一般文字（Inter + Noto Sans TC 混排）|
| `var(--font-mono)` | 程式碼、ID、技術 string（JetBrains Mono）|

數字一律加 `font-variant-numeric: tabular-nums`（讓位數對齊），或直接用 base.css 的 `.num` class。

### 2.3 形狀

| Token | 用途 |
|---|---|
| `var(--radius)` | 卡片圓角（12px）|
| `var(--radius-sm)` | 按鈕 / pill 圓角（8px）|
| `var(--shadow-sm)` | 一般卡片陰影 |
| `var(--shadow-md)` | 浮起來的卡片 / modal |

### 2.4 共用 utility class（在 base.css）

| Class | 用途 |
|---|---|
| `.card` | 標準卡片 surface + border + padding + shadow |
| `.card-hdr` + `.card-hdr h2` + `.meta` | 卡片內標題列 |
| `.pill .pill-crit/.pill-warn/.pill-ok/.pill-info/.pill-muted` | 嚴重程度標籤 |
| `.chips` + `.chip` | filter chip 群組 |
| `.num` | 數字 tabular-nums |
| `.mono` | monospace 字體 |
| `.empty-state` | 空狀態置中提示 |
| `.btn` | 標準按鈕 |
| `.live-dot` | 綠點 pulse |
| `.flash` | 跨 widget 跳轉高亮動畫 |

---

## 3. Body content · 怎麼組裝

### 3.1 內容鋪陳順序（軟性建議）

1. **Alert / banner**（若有 critical 訊息或方法論註記）
2. **KPI summary**（4-6 個總攬數字）
3. **Distribution / breakdown**（donut / bar_list / pivot_table）
4. **Detail table**（逐項列表 + 可展開）
5. **次要 / 趨勢**（timeline / heatmap）

不是死規定 — **依故事邏輯調整**。但通常「最大訊號在上、明細在下」最好讀。

### 3.2 用既有 widget 優先

| 場景 | 用哪個 widget |
|---|---|
| 一句話判斷 / 警示 | `alert` |
| 4-6 個總覽數字 | `kpi_grid` |
| 列表 + filter chips + 可展開細節 | `table` |
| 跨類別排名 / 比例 bar | `bar_list` |
| 比例（% of 100）| `donut` |
| 對標單一指標 vs 目標 | `gauge` |
| 簡短標籤群 | `chip_strip` |
| Org → network → device 樹 | `topology_tree` |
| 時間軸事件（到期 / 警示）| `timeline` |
| 2D matrix 熱區 | `heatmap` |
| **行列交叉表（type × org 之類）** | **`pivot_table`** ⭐ |
| **每行多 segment 堆疊 bar** | **`stacked_bar_list`** ⭐ |

### 3.3 既有 widget 不夠用時 → raw_html section

`compose.py` 支援 `{"raw_html": "..."}` 形式 section。當你判斷現有 widget 無法表達需要的視覺時：

```json
{
  "id": "my-custom-section",
  "raw_html": "<div class='card'><h2>自訂內容</h2>...</div>",
  "raw_html_reason": "為什麼選擇 hand-roll：[寫一句]。未來該抽象成什麼 widget：[寫一句]。"
}
```

**規則**：
- ✅ raw_html 內必須用 `var(--...)` tokens，**不能** hardcode 顏色/字體
- ✅ 必須填 `raw_html_reason` 解釋 trade-off — 累積這些 reason 就是「下個 widget 該補什麼」的需求單
- ✅ 可以用 `.card`、`.card-hdr`、`.pill` 等 base.css utility class
- ❌ 不要重寫 header / footer（compose.py 已包）
- ❌ 不要寫 inline `<script>` 改 DOM — 用 widget 機制或 runtime.js event bus
- ❌ 不要引外部 JS lib（Chart.js / D3）— 視覺一致性會崩

### 3.4 不超過 7 個 section

超過就拆兩張 dashboard。一張塞太多 = 客戶 30 秒內找不到重點。

---

## 4. 互動規範

### 4.1 Hover / focus

- Hover：`background: var(--surface-2)` 即可，不要用陰影 / scale 動畫
- 按鈕：`.btn` 內建 hover style，不要自己寫

### 4.2 跨 widget 跳轉

✅ 用 `bus.emit('navigate', { target: 'widget-id', filter: '...' })`
❌ 不要寫 inline `onclick="..."`

詳見 `runtime/runtime.js` 的 event bus 機制。

### 4.3 跳轉時的視覺回饋

跨 widget 跳轉時，目標 widget 套 `.flash` class（base.css 已定義金色 pulse 動畫）。runtime.js 內建這個行為。

### 4.4 KPI 卡點擊跳轉

`kpi_grid` widget 已支援。spec 內每個 KPI item 設 `click_target: "widget-id"` 即可。

---

## 5. i18n / Theme 相容性

### 5.1 i18n

⚠️ **不要** 把使用者看到的字串硬寫在 raw_html 裡。應該：

- Spec section level：用 `title` / `subtitle` / `meta` 屬性，這些可被 spec.locales 覆寫
- Widget level：所有可變字串包成 `config` 屬性
- 動態文字（runtime 算出）：用 `compute_fns` 放 spec.compute_fns，每個 locale 各自 override（見 examples/* 已驗證的 i18n pattern）

### 5.2 Theme（light / dark）

⚠️ **不要** 寫 `color: #047857`。**只能** 用 tokens：

```css
/* ❌ 錯 */
.my-thing { background: #f0f0f0; color: #333; border: 1px solid #ccc; }

/* ✅ 對 */
.my-thing { background: var(--surface); color: var(--text-1); border: 1px solid var(--border); }
```

切到 dark theme（`--theme dark`）時所有顏色自動 cascade，**不需要寫 dark mode CSS**。

---

## 6. 品質判斷 · 什麼是「好 dashboard」

對著最終輸出問自己：

1. **客戶 5 秒內**能看出「整體狀態好 vs 不好」？（用顏色 + alert + KPI）
2. **客戶 10 秒內**知道「最該處理的是哪個項目」？（用排名 / 突出視覺）
3. **客戶 30 秒內**能找到具體下一步？（用 table 展開 / action 按鈕）
4. 跨 dashboard 看起來像**同一個產品**？（design tokens 一致）
5. Section 數量 **≤ 7**？
6. **不超過 1 個** raw_html section？（多了表示 widget library 該擴張）

---

## 7. Output filename convention

Dashboard 輸出檔名走**雙模式**，根據是 validated（預錄）還是 ad-hoc（即興）：

### 7.1 Validated specs（穩定檔名）

對應 `examples/<topic>.spec.json` 的 dashboard 用穩定檔名，方便書籤、SI 給客戶分享：

| 檔名 pattern | 範例 | 用途 |
|---|---|---|
| `<topic>.html` | `org-health.html` | 預設語言版（zh-TW）|
| `<topic>-en.html` | `org-health-en.html` | 英文版 |
| `<topic>-ja.html` | `org-health-ja.html` | 日文版 |
| `<topic>-dark.html` | `org-health-dark.html` | Dark theme variant |

特性：可書籤、URL 可分享、會被覆蓋（每次重 compose 同一檔）。

### 7.2 Ad-hoc generation（永遠帶 timestamp）

當 AI 在對話中即興組 dashboard（不是跑 validated examples），**預設**用 timestamped 檔名：

```
canvas-<topic>-YYYYMMDD-HHMMSS.html
```

範例：`canvas-org-device-distribution-20260517-002928.html`

**為什麼一定要 timestamp**：

- ✅ **Wedge 證據**：booth 觀眾看到 URL 在變 = 證明「剛剛生的」，不是預錄
- ✅ **歷史保留**：每次生成保留一份，舊的不被蓋
- ✅ **配 generated-log.html**：log entry 對應 timestamped canvas，可追溯
- ❌ 如果固定檔名 → 觀眾看不出是 ad-hoc 還是 cached

### 7.3 操作員的指令模板

| 情境 | 跑什麼 |
|---|---|
| Booth 主秀（按腳本走）| `python compose.py --spec examples/<topic>.spec.json --out <topic>.html` |
| Booth 主秀多語 | `python compose.py --spec examples/<topic>.spec.json --locale ja --out <topic>-ja.html` |
| Booth ad-hoc（觀眾問新問題）| `python compose.py --spec /tmp/adhoc.spec.json --out canvas-<topic>-$(date +%Y%m%d-%H%M%S).html` |

---

## 8. Soft anti-patterns · 不建議但不會崩

> 跟 §🚫 Hard prohibitions 差別：§🚫 是「**遇到就停**」，§8 是「**儘量避免**」。下面是 UX / 品質類的常見錯誤，做了不會崩，但 dashboard 會差。

| 反 pattern | 為什麼不好 |
|---|---|
| 一頁塞 10+ section | 客戶找不到重點，掃描成本太高 |
| Section 之間留太大 margin | 視覺破碎，看不出哪些是相關的 |
| 把所有 KPI 數字塞 1 個 `kpi_grid`（超過 6 個）| 對手機 / 小螢幕崩 |
| 表格 row 沒辦法展開細節 | 客戶要點進另一個 widget 查 → 動線斷 |
| Donut 超過 6 個 segment | 顏色辨識度下降，legend 變超長 |
| Bar list 沒排序 | 一眼看不到「最大的是誰」 |
| Alert 文字超過 3 行 | 變成 paragraph，失去「一句話判斷」的本意 |
| 在 §🚫 的紅線邊緣寫 raw_html | 若不確定 → 不要寫，問使用者 |

---

## 9. 給 LLM 的執行 checklist

組 spec 之前自問：

```
先掃 §🚫:
[ ] 沒違反 9 條 hard prohibitions
[ ] 沒在 raw_html 放 secret / 引外部 lib / 寫 <script>

再規劃內容:
[ ] 我要表達的內容是什麼？（用一句話）
[ ] 這個內容用既有 widget 能表達嗎？
[ ] 如果不能，是哪個 widget 該補？我先用 raw_html 並寫 reason
[ ] Section 數量 ≤ 7？
[ ] 每個顏色用了 var(--...) tokens？
[ ] 字串都可以 i18n 覆寫？
[ ] 客戶 5/10/30 秒能找到什麼？

決定 output:
[ ] Validated → 穩定檔名（§7.1）
[ ] Ad-hoc → timestamped 檔名（§7.2）
```

---

## 10. 維護注意事項

- **§🚫 Hard prohibitions**：新發現的紅線加進來時，明確標明「會破壞 demo / 違法 / 系統會崩」其中哪一類
- **§3.2 widget 表**：新 widget 加進來時更新這裡 + `references/index.md`
- **§7 filename convention**：當有新的命名場景出現再補
- **§8 Soft anti-patterns**：累積踩坑後補
- **§3.3 raw_html_reason 累積分析**：每月 review 一次，看哪些 reason 重複 → 變成新 widget needs
- **目標長度**：≤ 450 行（每次 dashboard-builder 觸發都載入，token 成本控制）
