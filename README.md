# NetSense AI · Network Management Assistant Proposal

完整的 AI 網管助理產品提案資料 — **11 個頁面 + 4 個互動 mockup + 1 個 sales deck**。

🔗 **Live Demo**: 部署後此處放 Vercel URL

## 📂 從哪裡開始

打開 [`index.html`](./index.html) — 專案入口頁，依您的角色挑一個入口。

## 📚 內容結構

### 策略 / 故事層
- [`overview-pm-mkt.html`](./overview-pm-mkt.html) — PM/MKT 客戶故事（3 personas × 各自體驗）
- [`three-modes.html`](./three-modes.html) — 三模式產品定位（Mode A/B/C）
- [`system-diagram.html`](./system-diagram.html) — 高層次系統圖

### 規劃 / 工具層
- [`use-case-matrix.html`](./use-case-matrix.html) — 4 維度 × 3 模式使用案例矩陣
- [`playbook-examples.html`](./playbook-examples.html) — 5 個 playbook 範例

### 殺手功能
- [`dashboard-builder-demo.html`](./dashboard-builder-demo.html) — Dashboard Builder 4 場景 demo
- [`dashboard-builder-implementation.html`](./dashboard-builder-implementation.html) — 實作完整指南（4 tab）

### 技術深入
- [`architecture-v2-zh.html`](./architecture-v2-zh.html) — 系統架構（繁中互動版）
- [`architecture-v2.html`](./architecture-v2.html) — System Architecture (English)
- [`blind-spots.html`](./blind-spots.html) — 12 個工程盲點與對策

### UI Mockups（[`mockup-gallery.html`](./mockup-gallery.html) 統合入口）
- [`employee-chat-mockup.html`](./employee-chat-mockup.html) — Mode A 員工自助 chat
- [`cockpit-mockup.html`](./cockpit-mockup.html) — Mode B SMB IT Cockpit
- [`dashboard-builder-flow-mockup.html`](./dashboard-builder-flow-mockup.html) — Dashboard Builder 4 步驟
- [`mode-c-pro-mockup.html`](./mode-c-pro-mockup.html) — Mode C Pro Console（MSP）

### 對外簡報
- [`pitch-deck.html`](./pitch-deck.html) — 10 張投影片 sales pitch deck

## 🛠 技術細節

- **純靜態 HTML**：無 build 步驟、無 backend、無 framework
- **依賴**：僅 Google Fonts CDN（Inter / Noto Sans TC / JetBrains Mono）
- **離線可用**：CDN 不可達時也能基本顯示
- **互動**：所有 mockup 純 vanilla JS 實作，無外部 library

## 📐 設計系統

- 深色主題（`#0a1628` 為基底）
- 主色：橘 `#ff6b35`、青 `#00d9c5`
- 三模式色：青 / 橘 / 紫（A / B / C）
- 字體：Inter (Latin) + Noto Sans TC (中文) + JetBrains Mono (code)

## 📝 使用情境

| 對象 | 從哪頁開始 |
|---|---|
| PM / MKT / 業務 | `overview-pm-mkt.html` |
| 工程師 / Tech Lead | `architecture-v2-zh.html` |
| 產品定位 / 內部對焦 | `three-modes.html` |
| 排 roadmap | `use-case-matrix.html` |
| 看 UI 設計 | `mockup-gallery.html` |
| 技術買家 / CIO | `blind-spots.html` |
| 展會 / 對外 pitch | `pitch-deck.html` |

## 🤖 AI 協作

This proposal was iteratively designed and built with Claude.
