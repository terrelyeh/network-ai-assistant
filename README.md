# Network AI-Assistant · Network Management Assistant Proposal

完整的 AI 網管助理產品提案資料 — **10 個頁面 + 3 個互動 mockup + 1 個 sales deck**。

🔗 **Live**: https://network-ai-assistant.vercel.app

## 📂 從哪裡開始

打開 [`index.html`](./index.html) — 專案入口頁，依您的角色挑一個入口。

## 📚 內容結構

### 策略 / 故事層
- [`overview-pm-mkt.html`](./overview-pm-mkt.html) — PM/MKT 客戶故事（2 personas × 各自體驗）
- [`two-modes.html`](./two-modes.html) — 兩模式產品定位（Mode A 員工 / Mode B SMB IT）
- [`system-diagram.html`](./system-diagram.html) — 高層次系統圖

### 規劃 / 工具層
- [`use-case-matrix.html`](./use-case-matrix.html) — 4 維度 × 2 模式使用案例矩陣
- [`playbook-examples.html`](./playbook-examples.html) — 5 個 playbook 範例

### ⭐ Wedge Product（進入點產品）
- [`dashboard-builder-demo.html`](./dashboard-builder-demo.html) — 4 場景互動 demo
- [`dashboard-builder-implementation.html`](./dashboard-builder-implementation.html) — 實作完整指南（4 tab）

> Dashboard Builder 是**跨模式 wedge product**，不是 Mode B 子功能。
> 行銷上獨立主推、工程上仍是 third skill class。

### 技術深入
- [`architecture-v2-zh.html`](./architecture-v2-zh.html) ⇄ [`architecture-v2.html`](./architecture-v2.html) — 系統架構互動版（**頁內可切換 繁中 ⇄ EN**）
- [`blind-spots.html`](./blind-spots.html) — 12 個工程盲點與對策

### UI Mockups（[`mockup-gallery.html`](./mockup-gallery.html) 統合入口）
- [`employee-chat-mockup.html`](./employee-chat-mockup.html) — Mode A 員工自助 chat
- [`cockpit-mockup.html`](./cockpit-mockup.html) — Mode B SMB IT Cockpit
- [`dashboard-builder-flow-mockup.html`](./dashboard-builder-flow-mockup.html) — Dashboard Builder 4 步驟流程

### 對外簡報
- [`pitch-deck.html`](./pitch-deck.html) — 10 張投影片 sales pitch deck（主推 Dashboard Builder wedge）

## 🛠 技術細節

- **純靜態 HTML**：無 build 步驟、無 backend、無 framework
- **依賴**：僅 Google Fonts CDN（Inter / Noto Sans TC / JetBrains Mono）
- **離線可用**：CDN 不可達時也能基本顯示
- **互動**：所有 mockup 純 vanilla JS 實作，無外部 library
- **部署**：Vercel auto-deploy（push to main → 30 秒內 live）

## 📐 設計系統

- 深色主題（`#0a1628` 為基底）
- 主色：橘 `#ff6b35`、青 `#00d9c5`
- Mode 色：青 (A · 員工) / 橘 (B · SMB IT)
- Wedge 色：黃 `#fbbf24`（Dashboard Builder 專屬）
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
