# Network AI-Assistant · Network Management Assistant Proposal

完整的 AI 網管助理產品提案資料 — **11 個頁面 + 4 個互動 mockup + 1 個 sales deck + 3 份內部技術文件**，分成兩大入口：

- 🎯 **[home-product.html](./home-product.html)** — 產品 / 行銷（PM / MKT / 業務 / 經營層）· 淺色暖米調
- 🛠 **[home-engineering.html](./home-engineering.html)** — 工程 / 技術（Tech Lead / 工程師 / CIO）· 深色

兩側視覺刻意分流：行銷側對齊既有 EnGenius Cloud（白底 + sky blue + 橘），工程側維持深色技術調性。

🔗 **Live**: https://network-ai-assistant.vercel.app

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
- [`dashboard-builder-demo.html`](./dashboard-builder-demo.html) — 8 場景互動 demo（widget header 用 EnGenius Cloud logo，chat 側用品牌藍）
- [`dashboard-builder-implementation.html`](./dashboard-builder-implementation.html) — 實作完整指南（4 tab · 客戶/工程深入用）
- [`dashboard-builder-prep.html`](./dashboard-builder-prep.html) — ★ 前端準備指南（內部 kickoff 對齊 · sticky TOC + 右側滑入 design tokens panel）

> Dashboard Builder 是**跨模式 wedge product**，不是 Mode B 子功能。
> 行銷上獨立主推、工程上仍是 third skill class。

### 📄 內部技術文件（`docs/`）
- [`docs/widget-catalog.md`](./docs/widget-catalog.md) — 11 widget 完整規格（P0/P1/P2 三 tier · schema / 視覺 spec / LLM 使用時機）
- [`docs/prompt-templates.md`](./docs/prompt-templates.md) — LLM 系統提示模板 + 11 個 tool definitions + few-shot examples
- [`docs/dashboard-builder-implementation-guide.md`](./docs/dashboard-builder-implementation-guide.md) — 前端實作準備指南（人讀 markdown 版）
- [`docs/design-tokens.md`](./docs/design-tokens.md) — EnGenius Cloud design tokens（colors / typo / spacing / chart palette）

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
