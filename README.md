# Network AI-Assistant · Network Management Assistant Proposal

整合或開發兩條產品線：

- **Line 1** — 在既有 EnGenius Cloud 網管平台**內**整合 AI Chat 助理（員工自助 + SMB IT 駕駛艙）
- **Line 2** ⭐ **現 focus** — 把 Cloud API 包成 SKILL，給 AI coding agent（Claude Code）用，並基於情境**動態生成 dashboard**

🔗 **Live**: https://network-ai-assistant.vercel.app

## 🚀 開始這裡

### ⭐ Dashboard Builder（主秀，v0.2 · 2026-05-17 升級）
**[`dashboard-builder/architecture.html`](./dashboard-builder/architecture.html)** — 完整架構說明 v5（Persona + Design System）

- 跨真實 EnGenius Cloud staging API · 雙 script workflow（refresh-all + compose.py）
- **12 widget**（含 v0.2 新增 `pivot_table` + `stacked_bar_list`）· **6 validated 情境** · **3 locale**（zh-TW / EN / JA） · **light + dark theme**
- **AI 網管 persona**（[`skill/references/network-admin-persona.md`](./dashboard-builder/skill/references/network-admin-persona.md)）— Voice + 升級條件矩陣（文字 / dashboard / 動手 三種輸出形式自動選）
- **Design System 守則**（[`skill/references/design.md`](./dashboard-builder/skill/references/design.md)）— 3 層架構 + 9 條 hard prohibitions + raw_html escape hatch
- **Plugin install** — `dashboard-builder/skill/` 含 `.claude-plugin/` manifest，可被 Claude Code `/plugins install`
- 整套 skill 自包含在 [`dashboard-builder/skill/`](./dashboard-builder/skill/)（將來移交 RD 整合進 api-skills）

### 主要 hub 頁
- 🎯 [home-product.html](./home-product.html) — 產品 / 行銷 hub
- 🛠 [home-engineering.html](./home-engineering.html) — 工程 / 技術 hub
- 🧪 [prototype/scenarios.html](./prototype/scenarios.html) — 早期 PoC 展示集（2026-05-13 之前的版本）

## 📂 從哪裡開始

打開 [`index.html`](./index.html) — 主入口（2-card chooser），依您的角色挑一個 home。

## 📚 內容結構

### 策略 / 故事層
- [`overview-pm-mkt.html`](./overview-pm-mkt.html) — PM/MKT 客戶故事（2 personas × 各自體驗）
- [`two-modes.html`](./two-modes.html) — 兩模式產品定位（Mode A 員工 / Mode B SMB IT）
- [`system-diagram.html`](./system-diagram.html) — 高層次系統圖

### 規劃 / 工具層
- [`use-case-matrix.html`](./use-case-matrix.html) — 4 維度 × 2 模式使用案例矩陣
- [`playbook-examples.html`](./playbook-examples.html) — 5 個 playbook 範例

### ⭐ Wedge Product（進入點產品）

**主入口（2026-05 新建，最新進度）**：
- [`dashboard-builder/architecture.html`](./dashboard-builder/architecture.html) — 完整架構說明
- [`dashboard-builder/widget-catalog.html`](./dashboard-builder/widget-catalog.html) — 10 widget spec viewer
- 7 張 live dashboard：org-health / offboarding-audit / license-renewal / multi-org-governance / cross-org-reallocation（每張都有 zh-TW / EN / JA 三語言版 + light/dark theme）

**早期行銷頁（仍在站上，但內容對應的是 prototype，非 dashboard-builder）**：
- [`dashboard-builder-demo.html`](./dashboard-builder-demo.html) — 10 場景互動 demo
- [`dashboard-builder-implementation.html`](./dashboard-builder-implementation.html) — 實作完整指南（4 tab）
- [`dashboard-builder-prep.html`](./dashboard-builder-prep.html) — 前端準備指南

> Dashboard Builder 是**跨模式 wedge product**，不是 Mode B 子功能。
> 行銷上獨立主推、工程上仍是 third skill class。

### 📄 內部技術文件（`docs/`）

**Line 2（Dashboard Builder + SKILL）對齊文件**：
- [`docs/widget-catalog.md`](./docs/widget-catalog.md) — 12 widget 完整規格（P0/P1/P2 三 tier · schema / 視覺 spec / LLM 使用時機）
- [`docs/skill-to-widget-mapping.md`](./docs/skill-to-widget-mapping.md) ★ — widget ↔ 真實 op 對齊表 + RD action items + 場景對齊度
- [`docs/prompt-templates.md`](./docs/prompt-templates.md) — LLM 系統提示模板 + 12 tool definitions + few-shot examples
- [`docs/dashboard-builder-implementation-guide.md`](./docs/dashboard-builder-implementation-guide.md) — 前端實作準備指南
- [`docs/design-tokens.md`](./docs/design-tokens.md) — EnGenius Cloud design tokens

**展會 / Booth 用**：
- [`docs/booth-presenter-cheatsheet.md`](./docs/booth-presenter-cheatsheet.md) ★ — 操作員 1-page 操作指南（鍵盤 / talking script / 救命 5 條 / Q&A）
- [`docs/refine-demo-plan.md`](./docs/refine-demo-plan.md) — demo 互動擴充規劃

### 🧪 Live PoC（`prototype/`）

連真實 EnGenius Cloud staging API（`falcon.staging.engenius.ai`）跑通的 dashboard 集：

- [`prototype/scenarios.html`](./prototype/scenarios.html) ★ — Booth 操作員 menu
- [`prototype/canvas.html`](./prototype/canvas.html) — Multi-Org & License Audit
- [`prototype/canvas-network-audit.html`](./prototype/canvas-network-audit.html) — Network Config Audit (Gordon)
- [`prototype/canvas-team-access.html`](./prototype/canvas-team-access.html) — Team Access Audit
- [`prototype/generated-log.html`](./prototype/generated-log.html) — 自動 refresh log，每次 AI 生新 dashboard 都會跳新 entry（booth 觀眾看 productivity）
- [`prototype/booth-hospitality.html`](./prototype/booth-hospitality.html) — 5-phase 預錄飯店場景 demo（救命 backup）
- [`prototype/dashboard-live.html`](./prototype/dashboard-live.html) — 3-tab 整合版 PoC（含 LLM agent trace）
- [`prototype/live-data/*.json`](./prototype/live-data/) — 最新真實 API 回應

### 技術深入
- [`architecture-v2-zh.html`](./architecture-v2-zh.html) ⇄ [`architecture-v2.html`](./architecture-v2.html) — 系統架構互動版（**頁內可切換 繁中 ⇄ EN**）
- [`blind-spots.html`](./blind-spots.html) — 12 個工程盲點與對策

### UI Mockups（[`mockup-gallery.html`](./mockup-gallery.html) 統合入口）
- [`employee-chat-mockup.html`](./employee-chat-mockup.html) — Mode A 員工自助 chat（7 情境）
- [`cockpit-mockup.html`](./cockpit-mockup.html) — Mode B SMB IT Cockpit（4 情境切換）
- [`dashboard-builder-flow-mockup.html`](./dashboard-builder-flow-mockup.html) — Dashboard Builder 4 步驟流程（8 starter）
- [`unified-chat-mockup.html`](./unified-chat-mockup.html) — ★ Unified Chat PoC（一個 chat 三種 outcome · chat-first 產品方向）

### 對外簡報
- [`pitch-deck.html`](./pitch-deck.html) — 10 張投影片 sales pitch deck（主推 Dashboard Builder wedge）

## 🛠 技術細節

- **純靜態 HTML**：無 build 步驟、無 backend、無 framework
- **依賴**：僅 Google Fonts CDN（Inter / Noto Sans TC / JetBrains Mono）
- **離線可用**：CDN 不可達時也能基本顯示
- **互動**：所有 mockup 純 vanilla JS 實作，無外部 library
- **部署**：Vercel auto-deploy（push to main → 30 秒內 live）

## 📐 設計系統

兩套 palette 對應兩條敘事線：

### 🎯 Marketing 側（淺色 · 對齊 EnGenius Cloud）
- 底：暖米漸層 `#f5f2ea → #ebe6da`
- 主 accent：sky blue `#03A9F4`（EnGenius 品牌色）+ 橘 `#ff6b35`（Mode B）
- 卡片：純白 `#ffffff` + 暖咖啡 tint border + 微陰影
- 6 頁：home-product / overview-pm-mkt / two-modes / use-case-matrix / mockup-gallery / dashboard-builder-demo

### 🛠 Engineering 側（深色 · 技術調性）
- 底：深藍漸層 `#0a1628 → #0f1e3a`
- 主 accent：teal `#00d9c5` + 橘 `#ff6b35`
- 包含：所有 engineering hub 頁、`dashboard-builder-prep.html`、4 mockup 中的 `unified-chat-mockup.html`

### Mockup 視覺
3 個 mockup（cockpit / employee-chat / dashboard-builder-flow）跟 marketing 同 palette；
`unified-chat-mockup.html` 維持深色（chat-first 概念 PoC，獨立調性）。

### 共通
- Mode 色：cyan (A · 員工) / 橘 (B · SMB IT)
- Wedge 色：黃 `#fbbf24` / `#f59e0b`（Dashboard Builder 專屬）
- 字體：Inter (Latin) + Noto Sans TC (中文) + JetBrains Mono (code)

## 📝 使用情境

| 對象 | 從哪頁開始 |
|---|---|
| PM / MKT / 業務 | `overview-pm-mkt.html` |
| 工程師 / Tech Lead | `architecture-v2-zh.html`（含 EN 切換） |
| 產品策略 / 內部對焦 | `two-modes.html` |
| 排 roadmap | `use-case-matrix.html` |
| 看 UI 設計 | `mockup-gallery.html` |
| 技術買家 / CIO | `blind-spots.html` |
| 展會 / 對外 pitch | `pitch-deck.html` |

## 🚀 開發 / 維護

```bash
# 編輯檔案後
git add .
git commit -m "..."
git push
# Vercel 自動 redeploy ~30 秒內
```

開發注意事項與架構細節詳見 [`CLAUDE.md`](./CLAUDE.md)（給 AI session 接手用）。

## 🤖 AI 協作

This proposal was iteratively designed and built with Claude.
