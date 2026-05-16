# CLAUDE.md — Network AI-Assistant Proposal Site

> Last updated: 2026-05-16

## Project Overview

純靜態 HTML 產品提案網站 — 「**Network AI-Assistant**」AI 網管助理。
**目前 focus：Product Line 2（Dashboard Builder + EnGenius Cloud SKILLs）**。

完整功能與內容結構詳見 [README.md](README.md)。
**Live**: https://network-ai-assistant.vercel.app

## 🎯 兩條產品線（重要 — 兩線不要混）

| | Line 1 · Cloud-Embedded AI | **Line 2 · SKILL + AI Coding Agent ★ 現 focus** |
|---|---|---|
| 整合位置 | 既有 EnGenius Cloud GUI 內 | 外部 AI tool（Claude Code）打 API |
| 使用者 | 員工 / SMB IT（cloud 用戶）| 進階 user / SI / partner |
| 互動 | Chat box inside cloud | Skill call + dynamic dashboard |
| 主要對應檔 | mockup-gallery 4 mockups（employee/cockpit/unified-chat）| Dashboard Builder demo + 整個 `prototype/` PoC |
| 狀態 | 視覺 mockup 完成，整合未開始 | **PoC 已跑通真實 staging API** |

**ICP 不變**：A 員工 / B SMB IT 兩模式都涵蓋。Dashboard Builder = wedge product 跨模式。

## Tech Stack

- **純靜態 HTML**（無 build / framework / backend），CSS + JS inline 每個檔自包
- **Vanilla JS** for 所有互動
- **Google Fonts CDN**：Inter / Noto Sans TC / JetBrains Mono
- **部署**：Vercel（push to main → auto-redeploy ~30s）
- **GitHub**：terrelyeh/network-ai-assistant
- **PoC 跑真 API**：Python 3 + `uv` venv + `requests`（用 RD 給的 `api-skills/` 套件，本機 gitignored）

## Directory Structure

```
network-ai-assistant/
├── 14 個內容頁 HTML（index / home-product / home-engineering / overview-pm-mkt
│   / two-modes / system-diagram / use-case-matrix / mockup-gallery
│   / dashboard-builder-demo / dashboard-builder-implementation
│   / dashboard-builder-prep / architecture-v2-zh / architecture-v2
│   / playbook-examples / blind-spots / pitch-deck）
├── 4 個 mockup HTML（employee-chat / cockpit / dashboard-builder-flow / unified-chat）
├── assets/
│   ├── engenius-logo.png
│   ├── diagram-architecture-overview.png   一張高層次架構圖（給投影片用）
│   └── diagram-architecture-overview.svg   ↑ SVG 原檔
├── docs/                                   給 RD / 設計 / prompt eng 的對齊文件
│   ├── widget-catalog.md                   12 widgets 完整規格（P0/P1/P2）
│   ├── prompt-templates.md                 LLM system prompt + tool defs + few-shot
│   ├── dashboard-builder-implementation-guide.md  前端實作準備指南
│   ├── design-tokens.md                    EnGenius Cloud design tokens
│   ├── skill-to-widget-mapping.md          ★ widget ↔ op 對齊文件（含 RD action items）
│   ├── booth-presenter-cheatsheet.md       ★ 展會操作員 cheat sheet
│   └── refine-demo-plan.md                 demo refine 互動規劃
├── prototype/                              舊版 PoC + 展會用 dashboard（2026-05-13 之前）
│   ├── canvas.html                         Multi-Org Audit dashboard（真實 staging API）
│   ├── canvas-network-audit.html           Network Config Audit
│   ├── canvas-team-access.html             Team Access Audit
│   ├── canvas-<TS>.html                    Timestamped 新生 dashboard（demo workflow）
│   ├── scenarios.html                      Booth 操作員 menu（list 所有 canvas）
│   ├── generated-log.html                  ★ 自動 refresh 的「AI 今天生過什麼」log
│   ├── generated-manifest.json             ↑ 每生一張 dashboard 就 append entry
│   ├── booth-hospitality.html              預錄 5-phase 飯店場景 demo（純戲劇 backup）
│   ├── booth-data/hospitality.json         ↑ 合成假資料
│   ├── api-responses/*.json                早期保留的真實 API 回應
│   ├── live-data/*.json                    早期 PoC 用的 staging snapshot
│   ├── data.json                           dashboard-live.html 用的聚合 JSON
│   └── dashboard-live.html                 3-tab 整合版 PoC（含 LLM agent trace）
├── dashboard-builder/                      ★ 2026-05-15 ~ 16 session 的 widget 化架構（獨立區）
│   ├── README.md                           入口導讀
│   ├── architecture.html                   主說明頁（5 層 + 3 層分工 + Gallery）
│   ├── widget-catalog.html                 10 widget spec viewer（markdown render）
│   ├── *.html                              7 張 dashboard canvas（org-health / offboarding / license / multi-org / cross-org-realloc / dark mode）
│   ├── live-data/*.json                    最新 staging snapshot（refresh-all.sh 寫入）
│   ├── skill/                              dashboard-builder skill（待 RD 接手 → api-skills/）
│   │   ├── SKILL.md / scripts/compose.py / theme/ / widgets/ / runtime/ / references/ / examples/
│   ├── scripts/refresh-all.sh              一鍵刷新 6 個 live-data JSON（~14s）
│   ├── scripts/build_topology.sh           跨 5 org topology 聚合
│   ├── assets/shots/                       gallery 用的 canvas 截圖
│   └── docs/                               session-specific docs（architecture/ rd-handoff/ rd-priorities/ rd-meeting/）
└── api-skills/                             RD 給的 senao-api-skills v0.1.0（gitignored，本機用）
```

## Architecture & Data Flow

每個 HTML 檔**完全 self-contained**。

### 兩線視覺切分（不要混）

| 線 | 對應檔案 | Palette |
|---|---|---|
| 行銷（Line 2 對外故事） | home-product / overview-pm-mkt / two-modes / use-case-matrix / mockup-gallery / dashboard-builder-demo / **prototype/* 全部** / 3 個 light mockup | 淺色暖米 + sky blue `#03A9F4` |
| 工程（含 unified-chat） | home-engineering / architecture-v2*  / dashboard-builder-implementation / dashboard-builder-prep / playbook-examples / blind-spots / system-diagram / index / pitch-deck / unified-chat-mockup | 深色 + teal `#00d9c5` |

## Conventions

### 雙 Palette（重要）

```css
/* Marketing / Prototype 側 — 淺色暖米 */
--bg-1: #f5f2ea;   --bg-2: #ebe6da;   --surface: #ffffff;
--border: rgba(60,50,35,0.12);   --text: #1a2332;
--accent: #ff6b35;   --cyan: #03a9f4;   --warn: #f59e0b;

/* Engineering 側 — 深色 */
--bg-1: #0a1628;   --bg-2: #0f1e3a;   --surface: rgba(255,255,255,0.04);
--border: rgba(255,255,255,0.12);   --text: #f8fafc;
--accent: #ff6b35;   --cyan: #00d9c5;   --warn: #fbbf24;
```

### 顏色語義

| Cyan | Accent (橘) | Warn (黃) |
|---|---|---|
| Mode A · 員工 / brand link | Mode B · SMB IT / 主軸 | **Wedge product (Dashboard Builder)** |

### 命名 / Nav

- 品牌：**Network AI-Assistant**（`AI-Assistant` 部分用 `<span class="accent">` 標亮）
- HTML 檔名：kebab-case
- 大部分頁 nav：`<a class="nav-link muted-link" href="...">`
- 加新頁要更新所有內容頁 nav + index.html

## ★ Dashboard Builder Skill（Line 2 核心區）

整套 AI demo 內容隔離在 [`dashboard-builder/`](dashboard-builder/)，跟 root + `prototype/` 不混。
**主入口**：[`dashboard-builder/architecture.html`](dashboard-builder/architecture.html) — 完整架構說明 + gallery + 規範。

### 雙 script workflow

```bash
# 1) 展前撈最新 staging 資料（~14s）
bash dashboard-builder/scripts/refresh-all.sh

# 2) spec JSON → 自包含 HTML（~200ms）
python dashboard-builder/skill/scripts/compose.py \
  --spec dashboard-builder/skill/examples/<scenario>.spec.json \
  --out dashboard-builder/<name>.html \
  [--theme light|dark] [--locale en|ja]
```

`compose.py` 不打雲端、`refresh-all.sh` 不生 HTML，分工乾淨。詳見 architecture.html#howto。

### 目前狀態

- **10 widgets**：alert / kpi_grid / table / bar_list / donut / gauge / chip_strip / topology_tree / timeline / heatmap
- **5 validated specs**（S2 / S3 / S4 / S5 / S7） · 全部跑通真實 staging API
- **3 locales**：zh-TW（預設）/ en / ja · 每個 spec 內含 `locales` 區塊，`--locale ja` 切換
- **2 theme variants**：light + dark（`--theme dark`）
- **Booth 主入口** 全部用 dashboard-builder/，不再經過 prototype/

### Validated path 紀律（不可破）

每個要 booth demo 的情境必須：
1. 有 `spec.json` 在 `dashboard-builder/skill/examples/`
2. 跑過 `compose.py` 產出 HTML，視覺/互動/auto-poll 全 work
3. 用到的每個 op 都在 RD supported 範圍（無 🔴 troubleshoot ops）

→ 沒過 = 不准上 booth。詳見 `dashboard-builder/architecture.html#demo-readiness`。

### 3 層分工（不要混）

- **Primitives**（RD 擁有）— 13 data skills + dashboard-builder skill 內部零件
- **Orchestration** — Claude Code 本身（即時組裝；**不蓋 scenario skill 層**會殺掉 wedge）
- **Playbook** — markdown 文件（widget refs / spec examples / scenario candidates）

## ⚠️ RD 端阻擋項目

**P0（阻 booth 戲劇性 demo）**：
- `network-{ap,gateway,switch}-troubleshoot` 三個 skill 缺 `scripts/`
- 47 個 op 不能執行（subscribe_* / rpc_*）→ 阻 rpc_led_dance / rpc_kick_clients / cable_diag / 即時 client list 等
- 4 份推 RD 會議材料在 [`dashboard-builder/docs/rd-meeting/`](dashboard-builder/docs/rd-meeting/)

**P1（阻新 widget 類型）**：
- 沒有 history aggregation API → line_chart / sparkline / area_chart widget 沒法做
- 提議 endpoint shape 在 [`dashboard-builder/docs/rd-meeting/04-history-api-proposal.md`](dashboard-builder/docs/rd-meeting/04-history-api-proposal.md)

完整優先序表：[`dashboard-builder/docs/rd-priorities.md`](dashboard-builder/docs/rd-priorities.md)

## Current Status

功能清單與 demo 細節詳見 [`dashboard-builder/architecture.html`](dashboard-builder/architecture.html) 跟 [README.md](README.md)。

### 🔜 Next Steps（下個 session 焦點）

**Critical（卡 RD）**：
1. **RD 補 troubleshoot scripts** + **history aggregation API** — 解鎖 P0 + P1 整批 widget 類型
2. RD ready 後排第 2 次 meeting（[`rd-meeting/04-history-api-proposal.md`](dashboard-builder/docs/rd-meeting/04-history-api-proposal.md) 已備好）

**獨立可做（不等 RD）**：
3. **Dashboard 視覺風格優化** — widget UI 還可更精緻（特別是顏色/字距/留白；可改 `skill/theme/tokens.css` 一處 cascade 全 dashboard）
4. **新情境腦力激盪** — 找更吸睛、更有 wow 感的新 demo 故事，走 validated path pipeline 加入 examples/

### 🟡 Pending（次優先）
- 日文版需 native speaker review（目前 LLM 草稿）
- `dashboard-builder/skill/` 整合進 `api-skills/skills/dashboard-builder/`（P2 · [`docs/rd-handoff.md`](dashboard-builder/docs/rd-handoff.md)）
- 行銷頁 polish（Line 1 視覺 mockup）

## Common Pitfalls

### Site / Visual
1. **macOS sed 需 `-i ''`**
2. **架構檔有兩份（ZH + EN）** — 改要兩份都改
3. **每個 HTML 檔 self-contained** — sed across files 要全域
4. **`AI-Assistant` 才是 highlighted span**（不是 Network）
5. **Dashboard Builder 視覺色用 warn 黃**（wedge），不是 accent 橘
6. **Marketing 頁 `--cyan` 是 sky blue `#03A9F4`，engineering 頁是 teal `#00d9c5`** — hardcoded rgba 不能搞混
7. **Marketing 頁卡片底色要實色（#fff），不要 rgba 透明** — 淺底會糊
8. **3 個 mockup 已 light，unified-chat-mockup 仍 dark** — 是 deliberate
9. **JPEG screenshot tool 對淺色卡片在淺底壓縮會看不見** — 用 preview_eval + getComputedStyle 驗證
10. **dashboard-builder-prep.html 用 CSS counter 自動編號** — 不要手動改數字

### Line 2 / API SKILL
11. **api-skills/ 是 RD 給的 separate repo**（gitignored，不要 commit 它的內容）
12. **API key 千萬別 commit 到 git** — 永遠 export 到 env var
13. **Python http.server 對 `?_=timestamp` cache-buster 會 404**（query string 被當檔名一部份）— 用 `fetch(url, { cache: 'no-store' })`
14. **skill 的 stdout 會有 `AAAURL ...` debug print 汙染 JSON** — 要 pipe 過濾 `head -n+1 from { line` 之類的 clean function
15. **network-{ap,gateway,switch}-troubleshoot 3 個 skill 沒有 scripts/**（subscribe_* 不能執行）— 等 RD 補
16. **viewer 角色受 RBAC 限制**：能讀 network-level（SSID / policy / ACL），不能讀 org-level（inventory / licenses）。Gordon / ann-AP 因此 inventory 拿不到 → 用 Main_Org 或 Vertical Demo
17. **`get_inventory` / `get_licenses` 是 PRO plan only** — terrel org 因 BASIC 會回 402

### Dashboard Builder Skill（這 session 新踩）
18. **Nested `<a>` 自動 auto-close**（gallery-card 包 locale-pill 時踩到）— 外+內都要 link 必須用 wrapper div 隔開
19. **spec 的 `compute_fns` 在 widget scripts 之後執行**（compose.py 的 script 順序）— 因此 spec 可以 override 內建 computeFns，i18n 就是用這 trick
20. **compose.py `deep_merge` 對 sections 用 id-based merge** — spec `locales[locale].sections` 可只列要 override 的 section（partial 覆寫）
21. **Programmatic scroll 不會 fire scroll event**（preview tool 限制）— 用 IntersectionObserver 監聽 active 狀態
22. **dashboard-builder/ 跟 prototype/ 不互通**：canvas 內的 `live-data/` 是相對路徑，前者讀 `dashboard-builder/live-data/`、後者讀 `prototype/live-data/`

## 詳細文件

### ⭐ Dashboard Builder（本 session 新區，主要看這裡）
- [`dashboard-builder/README.md`](dashboard-builder/README.md) — 入口導讀
- [`dashboard-builder/architecture.html`](dashboard-builder/architecture.html) ★ — 完整架構說明（5 層 / 3 層分工 / gallery / 規範）
- [`dashboard-builder/widget-catalog.html`](dashboard-builder/widget-catalog.html) — 10 widget spec 即時 render
- [`dashboard-builder/docs/rd-priorities.md`](dashboard-builder/docs/rd-priorities.md) ★ — RD P0-P3 待補項目
- [`dashboard-builder/docs/rd-handoff.md`](dashboard-builder/docs/rd-handoff.md) — skill 整合進 api-skills/ 步驟
- [`dashboard-builder/docs/rd-meeting/`](dashboard-builder/docs/rd-meeting/) — 4 份推 RD 會議材料（agenda / ask-sheet / storyboard / history API 提案）
- [`dashboard-builder/docs/scenario-candidates.md`](dashboard-builder/docs/scenario-candidates.md) — 10 個情境腦力激盪

### Line 2 早期對齊文件（仍適用）
- [docs/widget-catalog.md](docs/widget-catalog.md) — 早期 12 widget 規格（vs 現在實作的 10 widgets）
- [docs/skill-to-widget-mapping.md](docs/skill-to-widget-mapping.md) — widget ↔ op 對齊
- [docs/booth-presenter-cheatsheet.md](docs/booth-presenter-cheatsheet.md) — 展會操作手冊
- [docs/design-tokens.md](docs/design-tokens.md) — EnGenius 視覺 tokens

### Line 1 視覺 mockup（暫停推進）
- `employee-chat-mockup.html` / `cockpit-mockup.html` / `unified-chat-mockup.html` — chat-style 對話

### 給人看的 overview
- [README.md](README.md)
