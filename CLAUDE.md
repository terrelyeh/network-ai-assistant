# CLAUDE.md — Network AI-Assistant Proposal Site

> Last updated: 2026-05-17

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
├── dashboard-builder/                      ★ v0.2（Persona-aware + Design System）
│   ├── README.md                           入口導讀
│   ├── architecture.html                   主說明頁（v5 · §00 產品全貌 · §02c Persona · §03f Design System · §04b 雙軌 Demo Readiness）
│   ├── widget-catalog.html                 12 widget spec viewer（markdown render）
│   ├── *.html                              17 張 dashboard canvas（5 情境 × 3 語言 + dark + ad-hoc canvas-*-TS.html）
│   ├── live-data/*.json                    最新 staging snapshot（refresh-all.sh 寫入）
│   ├── skill/                              dashboard-builder skill（v0.2 · 可被 /plugins install）
│   │   ├── SKILL.md                        MANDATORY-loads design.md（v3 措辭 + session cache OK）
│   │   ├── .claude-plugin/                 plugin manifest（marketplace.json + plugin.json）
│   │   ├── skills/dashboard-builder/       symlink dir for Claude Code skill discovery
│   │   ├── scripts/compose.py              支援 raw_html section + warning for missing raw_html_reason
│   │   ├── runtime/runtime.js              skip raw_html sections from widget lifecycle
│   │   ├── theme/{tokens.css,tokens-dark.css,base.css}  design tokens
│   │   ├── widgets/                        12 widget HTML partials
│   │   ├── references/                     persona.md + design.md + 12 widget refs + index.md
│   │   └── examples/                       6 validated spec JSON（S2/S3/S4/S5/S7 + org-device-distribution）
│   ├── scripts/refresh-all.sh              一鍵刷新 live-data JSON（~14s）
│   ├── scripts/build_topology.sh           跨 5 org topology 聚合
│   ├── assets/shots/                       gallery 用的 canvas 截圖
│   └── docs/
│       ├── persona-test-results.md         ★ 2026-05-16/17 實測對話紀錄 + 7 章節命中對照
│       ├── devlog.{md,html}                AI 工具開發案例分享（已上 ai-learning-notes）
│       ├── rd-handoff.md / rd-priorities.md
│       └── rd-meeting/                     5 份推 RD 會議材料（含 deck #5 Persona 提案）
└── api-skills/                             RD 給的 senao-api-skills v0.1.0（gitignored，本機 + plugin install）
    └── references/                         本機 sync 過去的 persona.md + design.md（讓 RD skill 也載入）
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

### 目前狀態（v0.2 · 2026-05-17）

- **12 widgets**：alert / kpi_grid / table / bar_list / **stacked_bar_list** / donut / gauge / **pivot_table** / chip_strip / topology_tree / timeline / heatmap（粗體為 v0.2 新增）
- **6 validated specs**（S2 / S3 / S4 / S5 / S7 + org-device-distribution）
- **3 locales**（zh-TW / en / ja）+ **2 theme variants**（light / dark）
- **raw_html section** — `compose.py` 新支援 escape hatch，AI 可手寫 HTML 但必須附 `raw_html_reason` 累積未來 widget 需求
- **plugin install** — `dashboard-builder/skill/` 有 `.claude-plugin/` manifest + `skills/<n>/` symlinks，可被 `/plugins install` 裝起來

### Demo Readiness · 雙軌制（v0.2 更新 · 不再「全部 validated」）

| 情境 | 用什麼 |
|---|---|
| **主秀** — 觀眾預期會看到的故事 | ✅ Validated path（5 個 examples）· 穩定檔名 `<topic>.html` |
| **Off-script** — 觀眾意外問問題 | ⚡ design.md 規範 ad-hoc 即興 · timestamped 檔名 `canvas-<topic>-YYYYMMDD-HHMMSS.html` |

詳見 `dashboard-builder/architecture.html#demo-readiness`。

### 知識架構（3 層 Playbook docs + 未來規劃）

| Layer | 文件 | 角色 |
|---|---|---|
| ✅ 1 | `references/network-admin-persona.md` (358 行) | Voice + 升級條件 · 每次 skill 觸發都載入 |
| ✅ 2 | `references/design.md` (341 行) | 視覺設計守則 · §🚫 9 條 hard prohibitions + raw_html 規則 · dashboard-builder 觸發時載入 |
| 🔜 3 | `references/house-rules.md` (未寫) | EnGenius 品牌觀點（HVS 分數、推薦原則）· 需 RD + 業務共寫 |
| 🔜 4 | `references/playbooks/{configure,troubleshoot,monitor}.md` (未寫) | 任務型 mental model · 條件式載入 |
| 🔜 5 | `memory/<org-id>.md` (未設計) | 跨 session 記憶 · 等真實 SI 使用後再設計 |

### 3 層執行分工（不要混 · v0.2 仍適用）

- **Primitives**（RD 擁有）— 13 data skills + dashboard-builder skill 內部零件 + widget library
- **Orchestration** — Claude Code 本身（即時組裝；**不蓋 scenario skill 層**會殺掉 wedge）
- **Playbook** — markdown 文件（persona.md + design.md + widget refs + spec examples + 未來 house-rules / playbooks）

### Plugin install / cache sync workflow

**裝 plugin**：`/plugins` → Add marketplace（指向 `api-skills/` 或 `dashboard-builder/skill/`）→ Install plugin → User scope → 重啟 Claude Code。

**改完 SKILL.md / design.md / widgets 後**（Claude Code 不會自動 refresh）：
```bash
# 同步 plugin cache（最快）
SRC=dashboard-builder/skill
CACHE=~/.claude/plugins/cache/dashboard-builder/dashboard-builder/0.1.0
cp $SRC/SKILL.md $CACHE/
cp -R $SRC/references/* $CACHE/references/
cp $SRC/widgets/*.html $CACHE/widgets/
cp $SRC/scripts/*.py $CACHE/scripts/
cp $SRC/runtime/*.js $CACHE/runtime/
cp $SRC/examples/*.json $CACHE/examples/

# Or: /plugins → Uninstall + Reinstall（乾淨但慢）
```

→ 然後 `/clear` 或重啟 Claude Code 讓對話重新 load。

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

**下個 session 主軸（user 指定）**：
1. **任務型 playbooks 思考模型細節討論** — 設計 `references/playbooks/{configure,troubleshoot,monitor}.md` 的具體內容。原則：寫成 **mental model**（思考骨架 / 診斷維度 / 詢問三定問）而非 **script**（first do X, then Y）— script 會凍結 AI 判斷 = 蓋 scenario skill 層 = 殺 wedge。
2. **memory.md 方向與細節** — 設計跨 session 記憶機制。4 種 memory 類型已釐清（project / conversation / customer / user）。SI 場景最需要 ③ customer memory，但需設計：per-org-id namespace、stale TTL、隱私 / 多客戶切換、何時讀 / 何時寫。**等真實 SI 使用 1-2 個月後再實作**比較不會猜錯。

**Critical（仍卡 RD）**：
3. **RD 補 troubleshoot scripts**（5 個 P0 op：rpc_led_dance / rpc_kick_clients / subscribe_client_list / subscribe_cable_diag / rpc_reboot）+ **history aggregation API** — 解鎖 P0 demo + line_chart / sparkline widget 類型
4. RD ready 後排第 2 次 meeting（[`rd-meeting/04-history-api-proposal.md`](dashboard-builder/docs/rd-meeting/04-history-api-proposal.md) + 第 2 次帶 [`rd-meeting/05-persona-proposal.md`](dashboard-builder/docs/rd-meeting/05-persona-proposal.md)）

**獨立可做（不等 RD）**：
5. **寫 `house-rules.md` v0** — Layer 3 知識架構最後拼圖（EnGenius 品牌觀點 · HVS 分數區間 / 平台特有 gotcha）
6. 新情境腦力激盪 — 找更吸睛的新 demo 故事，走 validated path pipeline 加 examples/

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

### Dashboard Builder Skill
18. **Nested `<a>` 自動 auto-close**（gallery-card 包 locale-pill 時踩到）— 外+內都要 link 必須用 wrapper div 隔開
19. **spec 的 `compute_fns` 在 widget scripts 之後執行**（compose.py 的 script 順序）— 因此 spec 可以 override 內建 computeFns，i18n 就是用這 trick
20. **compose.py `deep_merge` 對 sections 用 id-based merge** — spec `locales[locale].sections` 可只列要 override 的 section（partial 覆寫）
21. **Programmatic scroll 不會 fire scroll event**（preview tool 限制）— 用 IntersectionObserver 監聽 active 狀態
22. **dashboard-builder/ 跟 prototype/ 不互通**：canvas 內的 `live-data/` 是相對路徑，前者讀 `dashboard-builder/live-data/`、後者讀 `prototype/live-data/`

### Plugin / Persona / Design 機制（v0.2 新踩）
23. **Plugin install 會 COPY 不是 symlink** — 改 SKILL.md / design.md 後 `~/.claude/plugins/cache/<plugin>/<version>/` 不會自動更新，要手動 sync 或 `/plugins` reinstall
24. **Plugin install 後要重啟 Claude Code** — 不是 `/clear`，是完全 quit 重開，才會 re-scan `/skills` 清單
25. **SKILL.md MANDATORY 措辭 v1 太軟、v2 太硬、v3 才對齊**：「session 首次必讀 · 後續可用 context · 但要透明說明」— 強制每次重讀會 Claude 違反規則（合理 token 優化）
26. **persona / design.md 改動要 sync 到 3 個地方**：worktree（git）+ main repo（如果還用）+ `api-skills/references/` + `~/.claude/plugins/cache/`（每次手動 cp）
27. **Worktree 路徑陷阱**：Write/Edit 工具如果用絕對路徑會寫到 main repo，不是 worktree。`git diff` 看不到變化 — 要用 `git -C <worktree>` 或相對路徑
28. **dashboard-builder 是 plugin · 結構要 `skills/<n>/SKILL.md`**：Claude Code 不支援 SKILL.md at plugin root，需要 `skills/dashboard-builder/` 子目錄（用 symlinks 回上層保持單一檔案來源）
29. **raw_html section 必須有 `raw_html_reason`** — compose.py 沒填會 print warning。寫的目的是累積「下一個 widget 該補什麼」的需求單（self-improving library）
30. **Symlinks 在 git 跨平台**：worktree 的 `skills/dashboard-builder/` 用 symlinks 指回上層，git 會以 `120000` mode 保存。macOS / Linux work，Windows checkout 會變一般檔（未來 RD 接手要注意）

## 詳細文件

### ⭐ Dashboard Builder（主要看這裡）
- [`dashboard-builder/architecture.html`](dashboard-builder/architecture.html) ★ — 完整架構（v5 · §00 產品全貌 · §02c Persona · §03f Design System · §04b 雙軌 Demo Readiness）
- [`dashboard-builder/skill/references/network-admin-persona.md`](dashboard-builder/skill/references/network-admin-persona.md) ★ — Voice + 升級條件
- [`dashboard-builder/skill/references/design.md`](dashboard-builder/skill/references/design.md) ★ — Dashboard 設計守則 v0.2（含 §🚫 9 條 hard prohibitions）
- [`dashboard-builder/widget-catalog.html`](dashboard-builder/widget-catalog.html) — 12 widget spec 即時 render
- [`dashboard-builder/docs/persona-test-results.md`](dashboard-builder/docs/persona-test-results.md) ★ — 2026-05-16/17 實測對話 + 7 章節命中對照
- [`dashboard-builder/docs/devlog.{md,html}`](dashboard-builder/docs/) — AI 工具開發案例分享（已上 ai-learning-notes repo）
- [`dashboard-builder/docs/rd-priorities.md`](dashboard-builder/docs/rd-priorities.md) — RD P0-P3 待補項目
- [`dashboard-builder/docs/rd-handoff.md`](dashboard-builder/docs/rd-handoff.md) — skill 整合進 api-skills/ 步驟
- [`dashboard-builder/docs/rd-meeting/`](dashboard-builder/docs/rd-meeting/) — 5 份推 RD 會議材料（含 deck #5 Persona 提案）
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
