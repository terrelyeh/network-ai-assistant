# CLAUDE.md — Network AI-Assistant Proposal Site

> Last updated: 2026-05-13

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

## 🎯 Line 2 PoC 現況（Dashboard Builder 工作流）

**目標**：訪客問問題 → 操作員跑 SKILL → AI 用真實 API 結果生 dashboard HTML →
preview 視窗顯示 → 觀眾看到 wow。

### 已跑通的 6 個真實 API ops（讀取類）

```python
# 在 api-skills/ 目錄，已驗證 staging 可呼叫：
init-orgs/get_user_orgs           # 5 orgs
hvs/get_hierarchy_views           # 14 networks (Gordon 含 7F_shieldingRoom)
org-devices/get_inventory         # 1 device (Vertical Demo / ESG610 gateway)
org-licenses/get_licenses         # 3 licenses (1 expired)
networks/get_ssid_profiles        # 1 SSID
networks/get_general_policy_plus  # 32 policy fields
networks/get_network_acls         # all 3 access types empty
team-members/get_org_memberships_overall  # 3 members (黃依雯/Antony/Terrel)
```

### 已驗證流程

```bash
cd api-skills && source .venv/bin/activate
export MANAGE_SYSTEM_URL="https://falcon.staging.engenius.ai"
export API_KEY="<從 user 帳號生成>"
# 跑 skill → JSON → 我讀 → 寫 canvas-<TS>.html → preview 自動顯示
```

### Booth 展會工作流（驗證 work）

```
prototype/generated-log.html ── (auto-poll 2s) ──┐
                                                  │
[訪客問問題]                                       │
   ↓                                              │
[操作員] Claude Code 跑 skill                     │
   ↓                                              │
[操作員] 告訴我「生 X 場景」                      │
   ↓                                              │
[我] 寫 canvas-<TS>.html + 加 entry 到 manifest   │
   ↓ ────────────────────────────────────────────┘
[generated-log] 新 entry 綠光 fresh 動畫，counter +1
```

## ⚠️ 重要：Line 2 SKILL 限制（2026-05-13 確認）

### 能跑（有 scripts/）

`init-orgs / hvs / networks / org-devices / org-licenses / org-network-groups /
org-network-templates / org-backups / team-members / engenius-env`

### 不能跑（只有 SKILL.md 文件，沒有 scripts/）

`network-ap-troubleshoot / network-gateway-troubleshoot / network-switch-troubleshoot`

→ subscribe_stat / subscribe_throughput / subscribe_channel_utilization 等
**即時監控類 op 目前不能執行**。要 RD 補 scripts/ 才能做 Level 2「watch this tick」live demo。
**Dolphin 平台支援也還在 RD 開發中**。

### 影響的 demo 場景

- ✅ 能做：Multi-org audit / Network config audit / License lifecycle / Team access — 都是讀取類 GET ops
- ❌ 不能做：Real-time AP health / Live throughput / Sticky client hunt — 需要 subscribe_*
- ❌ 不能做：歷史聚合（過去 N 天趨勢）— 沒有 history API

## Current Status

### ✅ 已完成（Line 2 PoC）
- senao-api-skills 跑通 real falcon.staging API（6+ GET ops）
- 4 個 canvas dashboard（multi-org / network audit / team access / license renewal）
- scenarios.html booth menu
- generated-log.html 自動 refresh 的歷史 log
- booth-hospitality.html 預錄版（救命 backup）
- alignment doc + cheat sheet 完整

### 🔜 Next Steps（Line 2 focus）

優先：
1. **dry-run 真實 booth 流程** — 模擬訪客問題 → 跑 skill → 生 dashboard → log 跳新 entry
2. **擴 vertical 場景** — 不限飯店，按真實 staging 資料能做的（multi-org audit / security audit / license / team access 等）
3. **跟 RD 對齊** — 缺的 troubleshoot scripts + 歷史 API（Dolphin 補丁也是）
4. **booth presenter dry-run** — 用 cheat sheet 演練 3 遍 90 秒主秀

次優先：
- Vercel deploy 對應的 marketing 頁面 polish（行銷部分先擺著）

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
15. **network-{ap,gateway,switch}-troubleshoot 3 個 skill 沒有 scripts/**，只有 SKILL.md。subscribe_* 都不能執行（要 RD 補）
16. **viewer 角色受 RBAC 限制**：能讀 network-level（SSID / policy / ACL），不能讀 org-level（inventory / licenses）。Gordon org 因此 inventory 拿不到，要拿其他 org（Vertical Demo）的 inventory demo
17. **`get_inventory` / `get_licenses` 是 PRO plan only** — terrel org 因 BASIC 會回 402
18. **canvas-<TS>.html 生成後要 append manifest entry**，否則 generated-log 不會顯示

## 詳細文件

### Line 2 對齊文件（給 RD / Prompt Eng / Design）
- [docs/widget-catalog.md](docs/widget-catalog.md) — 12 widget 規格
- [docs/skill-to-widget-mapping.md](docs/skill-to-widget-mapping.md) ★ — widget ↔ op 對齊
- [docs/dashboard-builder-implementation-guide.md](docs/dashboard-builder-implementation-guide.md) — kickoff 對齊
- [docs/prompt-templates.md](docs/prompt-templates.md) — LLM prompt + tool defs
- [docs/design-tokens.md](docs/design-tokens.md) — EnGenius 視覺 tokens
- [docs/booth-presenter-cheatsheet.md](docs/booth-presenter-cheatsheet.md) ★ — 展會操作手冊
- [docs/refine-demo-plan.md](docs/refine-demo-plan.md) — demo 互動擴充

### Line 1 視覺 mockup（暫停推進）
- `employee-chat-mockup.html` / `cockpit-mockup.html` / `unified-chat-mockup.html` — chat-style 對話

### 給人看的 overview
- [README.md](README.md)
