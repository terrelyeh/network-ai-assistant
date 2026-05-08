# CLAUDE.md — Network AI-Assistant Proposal Site

> Last updated: 2026-05-06

## Project Overview

純靜態 HTML 產品提案網站 — 「**Network AI-Assistant**」AI 網管助理的完整提案資料包。
11 個策略/技術頁 + 4 個互動式 UI mockup + 1 份 sales pitch deck + 3 份內部技術文件（`docs/`），
部署於 Vercel。給 PM / MKT / Eng / 客戶 / 經營層不同對象用。

**ICP focus**：deliberately 兩模式 — A 員工 / B SMB IT。不做 MSP / multi-tenant / Pro Console。
架構保留 mode-agnostic，未來真要擴後端不會大改，但 marketing/positioning 不出現 Mode C。

**Brand alignment**（2026-05 加入）：行銷側對齊既有 EnGenius Cloud GUI（白/暖米底 + sky blue
`#03A9F4` + 橘 accent）；工程側維持原本深色（深藍底 + teal cyan + 橘 accent）。**兩套 palette 不要混**。

完整功能與內容結構詳見 [README.md](README.md)。
**Live**: https://network-ai-assistant.vercel.app

## Tech Stack

- **純靜態 HTML**（無 build 步驟、無 framework、無 backend）
- **Vanilla JS** for 所有互動（tabs、modals、chat、Cmd+K palette）
- **Google Fonts CDN**：Inter / Noto Sans TC / JetBrains Mono
- **部署**：Vercel（push to main → auto-redeploy ~30s）
- **GitHub**：terrelyeh/network-ai-assistant

## Directory Structure

```
network-ai-assistant/
├── index.html                                主入口（2-card chooser → product or engineering home）
├── home-product.html                         產品 / 行銷 hub（PM/MKT/業務）· 淺色暖米底
├── home-engineering.html                     工程 / 技術 hub（Tech Lead/CIO）· 深色
├── overview-pm-mkt.html                      PM/MKT 客戶故事
├── two-modes.html                            產品策略定位（A/B 兩模式）
├── system-diagram.html                       高層次系統圖（兩 hub 共用橋接）
├── use-case-matrix.html                      4×2 use case 矩陣
├── dashboard-builder-demo.html               Dashboard Builder 互動 demo（widget 用 EnGenius logo）
├── dashboard-builder-implementation.html     Dashboard Builder 實作指南（4-tab）
├── dashboard-builder-prep.html               ★ NEW · Dashboard Builder 前端準備指南（sticky TOC + scrollspy + 右側滑入 design tokens panel）
├── mockup-gallery.html                       4 mockup 統合入口
├── architecture-v2-zh.html / architecture-v2.html  互動架構圖（ZH ⇄ EN 切換）
├── playbook-examples.html                    5 個 playbook 範例
├── blind-spots.html                          12 個工程盲點
├── pitch-deck.html                           10-slide sales deck
├── *-mockup.html (4)                         互動式 mockup（員工 chat / cockpit / Dashboard Builder flow / Unified Chat PoC）
├── assets/
│   └── engenius-logo.png                     公司 logo（dashboard-builder-demo widget header 用）
└── docs/                                     內部技術文件（Markdown source）
    ├── widget-catalog.md                     11 widget 完整規格（P0/P1/P2 · 給 PM/RD/Design）
    ├── prompt-templates.md                   LLM system prompt 模板 + 11 tool defs + few-shot
    ├── dashboard-builder-implementation-guide.md  前端實作準備指南（人讀 markdown 版）
    └── design-tokens.md                      EnGenius Cloud design tokens（colors / typo / spacing / chart palette）
```

## Architecture & Data Flow

每個 HTML 檔**完全 self-contained**（CSS + JS 都 inline，無共用 assets）。
這代表：改一個檔案不影響其他，但加 CSS token / 共用樣式時要 manually sync。

### 兩套 nav 風格

| 類型 | 應用 | 結構 |
|---|---|---|
| **內容頁 nav** | 10 個策略/技術頁 | `<header>` 含 `.nav-links`，list 10 個 page link |
| **Mockup banner** | 4 個 mockup 檔 | 頂部 `.mockup-banner` 單一「← 回 Mockup 列表」連結 |

### 關鍵 framing（已穩定，不要回頭混淆）

- **3 個 home page**：`index.html` (chooser) → `home-product.html` (PM/MKT) 或 `home-engineering.html` (Tech)。`system-diagram.html` 兩邊都連結到（橋接）
- **2 modes** = 依「誰用」（user role）分：A 員工 / B SMB IT。**不做 Mode C / MSP**（不同 ICP）
- **Dashboard Builder = wedge product**（不是 Mode B 子功能）— 跨兩個模式可用，藍海競爭
- **4 dimensions** = 用例維度：Deployment / Monitoring / Troubleshoot / Management
- 工程上 Dashboard Builder 仍是 **third skill class**（與 Diagnostic / Monitoring playbooks 並列），架構不變
- Marketing 上 Dashboard Builder **獨立成 wedge** 主推（跨模式可用，藍海競爭）
- 架構保留 mode-agnostic — 未來真要擴 Mode C / MSP，後端不會大改

## Conventions

### 雙 Palette（重要 — 不要混）

從 2026-05 起整站分兩套 palette。**改檔前先確認該檔是 marketing 側還是 engineering 側**。

#### 🎯 Marketing side（淺色暖米）

6 個檔：`home-product.html` / `overview-pm-mkt.html` / `two-modes.html` / `use-case-matrix.html` /
`mockup-gallery.html` / `dashboard-builder-demo.html`

```css
--bg-1: #f5f2ea;             /* 暖米底 */
--bg-2: #ebe6da;             /* 暖米漸層 */
--surface: #ffffff;          /* 卡片純白 */
--surface-2: #faf8f3;
--border: rgba(60,50,35,0.12);  /* 暖咖啡 tint */
--text: #1a2332;             /* 深海軍藍（不是純黑） */
--muted: #5a6878;
--accent: #ff6b35;           /* 橘 · 保留 */
--cyan: #03a9f4;             /* ★ EnGenius sky blue */
--warn: #f59e0b;             /* 黃（略深於工程側）*/
```

#### 🛠 Engineering side（深色）

其他所有頁（`home-engineering.html` / `architecture-v2*.html` / `dashboard-builder-implementation.html` /
`dashboard-builder-prep.html` / `playbook-examples.html` / `blind-spots.html` / `system-diagram.html` / `index.html` /
`pitch-deck.html` / 4 mockup）

```css
--bg-1: #0a1628;             /* 深藍底 */
--bg-2: #0f1e3a;
--surface: rgba(255,255,255,0.04);
--border: rgba(255,255,255,0.12);
--text: #f8fafc;
--accent: #ff6b35;           /* 橘 · 主色 / Mode B */
--cyan: #00d9c5;             /* teal / Mode A / links */
--warn: #fbbf24;             /* 黃 / Wedge */
```

### 顏色語義（兩側共通）

| 顏色 | 對應 | 例 |
|---|---|---|
| Cyan | Mode A · 員工 / brand link | employee-chat-mockup（teal）/ marketing 頁的 link（sky blue）|
| Accent (橘) | Mode B · SMB IT · 主軸 | cockpit-mockup |
| **Warn (黃)** | **Wedge product (Dashboard Builder)** | dashboard-builder-demo / flow |

### Mockup 視覺現況（2026-05 更新）

3 個 mockup 已翻成 light + sky blue（跟 marketing 同 palette），只剩 1 個保留深色：

| Mockup | 視覺 |
|---|---|
| `cockpit-mockup.html` | 🎯 Light（cream + sky blue） |
| `employee-chat-mockup.html` | 🎯 Light |
| `dashboard-builder-flow-mockup.html` | 🎯 Light |
| `unified-chat-mockup.html` | 🛠 **保留深色**（user 決定不翻） |

整個 site 視覺線：marketing pages → 3 個 mockup → wedge demo → engineering docs 都是 light EnGenius 風格；
只有 `unified-chat-mockup.html` 跟所有 engineering 頁是深色。改其中一邊不要動到另一邊。

### 命名

- 品牌：**Network AI-Assistant** — `AI-Assistant` 部分用 `<span class="accent">` 標亮
- HTML 檔名：kebab-case
- 中英混用 OK，但對外面向（hero / titles）優先繁中

### Nav links 編輯時注意

- 大部分頁用 `<a class="nav-link muted-link" href="...">`（非 current 狀態）
- `architecture-v2-zh.html` / `architecture-v2.html` 例外用 `<a class="nav-link" href="...">`（無 muted-link）
- `dashboard-builder-prep.html` 用簡化的 3-link top nav（主入口 / 產品入口 / 工程入口），不重複內容頁的全 list
- 縮排不一致：mockup-gallery 用 4 spaces，architecture 用 6 spaces
- 加新頁時要更新**所有 9 個內容頁** + index.html（mockup 不需更新 nav）

## Current Status

功能清單詳見 [README.md](README.md)。

### 🔜 Next Steps（無使用者明確指定，視需要）

- 真實 design partner 試用驗證 wedge thesis
- 客製 domain（取代 Vercel default）
- OG image / social preview meta tags
- 加入 Vercel Analytics（看流量）
- 補 Mode A 員工 chat 的更多 playbook 範例
- `docs/widget-catalog.md` schema 用 Zod 寫成 TypeScript 範例檔（給 RD starter）

## Deployment

```bash
# 改 HTML → push → Vercel auto-redeploy
git add .
git commit -m "..."
git push
# 30-60 秒後 live: https://network-ai-assistant.vercel.app
```

驗證：
```bash
curl -sS -o /dev/null -w "%{http_code}\n" https://network-ai-assistant.vercel.app
```

## Common Pitfalls

1. **macOS sed 需 `-i ''`** — 不是 GNU sed，in-place 要 empty string 參數
2. **架構檔有兩份（ZH + EN）** — 改架構內容要兩份都改，否則 EN 會落後
3. **每個 HTML 檔是 self-contained** — 改 CSS token 不會影響其他檔，要全域改要 sed across files
4. **Mockup 的「回」連結指向 gallery** 而不是 index — 別誤改回 index
5. **`AI-Assistant` 才是 highlighted span**（不是 Network）— 改 brand 文字時注意 span 結構
6. **Dashboard Builder 視覺色用 warn (黃)** 不是 accent (橘)，因為它是 wedge 不是 Mode B 子功能
7. **加新頁要更新 nav + index.html**（resource cards、files table、count）— 漏一處會不一致
8. **index.html 的 page count 出現在 3 個位置**：hero meta、resources section title、各種 narrative 文字
9. **不要把 mockup 加進內容頁 nav 列表** — mockup 只從 mockup-gallery 進入
10. **檔案列表表格用 `⇄` 符號**（U+21C4）標明 ZH ⇄ EN 兩個檔案是 mirror
11. **Marketing 頁的 `--cyan` 是 `#03A9F4` sky blue** — 不是 engineering 側的 `#00d9c5` teal。
    在 marketing 檔裡看到 hardcoded `rgba(0,217,197,...)` 一定要改成 `rgba(3,169,244,...)`，反之亦然
12. **Marketing 頁卡片底色要用實色（如 `#ffffff`）**，不要用 `rgba(...)` 透明色 — 在淺底上會跟頁面 bg 幾乎同色
13. **Mockup 視覺要對 palette**：3 個 mockup 已翻 light（cockpit / employee-chat / dashboard-builder-flow），
    `unified-chat-mockup.html` 仍是深色 — 改 marketing 不會影響 mockup（self-contained），但 hardcoded
    `rgba(0,217,197,...)` 之類的 cyan 值在 light mockup 是 `rgba(3,169,244,...)`，別搞錯
14. **JPEG 截圖 tool 對淺色卡片在淺底上會壓縮到看不見**（rgba alpha 卡片尤其明顯）— 不是 bug，是 preview 限制；
    要用 `preview_eval` + `getComputedStyle` / `elementFromPoint` 驗證，別只信 screenshot
15. **`dashboard-builder-prep.html` 用 CSS counter 自動編號 section** — `<span class="num"></span>` 是空殼，數字由 `::before counter()` 產
    新增/刪除 section 不用改數字，但 TOC 那邊的 `<li>` 順序要對

## 詳細文件

- [README.md](README.md) — 給人看的功能介紹、檔案清單、使用情境
