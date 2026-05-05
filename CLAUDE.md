# CLAUDE.md — Network AI-Assistant Proposal Site

> Last updated: 2026-05-08

## Project Overview

純靜態 HTML 產品提案網站 — 「**Network AI-Assistant**」AI 網管助理的完整提案資料包。
12 個策略/技術頁 + 4 個互動式 UI mockup + 1 份 sales pitch deck，部署於 Vercel，
給 PM / MKT / Eng / 客戶 / 經營層不同對象用。

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
├── index.html                                專案入口（audience cards + resources）
├── overview-pm-mkt.html                      PM/MKT 客戶故事
├── three-modes.html                          產品策略定位（A/B/C 模式）
├── system-diagram.html                       高層次系統圖
├── use-case-matrix.html                      4×3 use case 矩陣
├── dashboard-builder-demo.html               Dashboard Builder 互動 demo
├── dashboard-builder-product.html            ⭐ Wedge product 定位（TAM/競品/freemium）
├── dashboard-builder-implementation.html     Dashboard Builder 實作指南（4-tab）
├── mockup-gallery.html                       4 mockup 統合入口
├── architecture-v2-zh.html / architecture-v2.html  互動架構圖（ZH ⇄ EN 切換）
├── playbook-examples.html                    5 個 playbook 範例
├── blind-spots.html                          12 個工程盲點
├── pitch-deck.html                           10-slide sales deck
└── *-mockup.html (4)                         互動式 mockup（Mode A/B/C + Dashboard flow）
```

## Architecture & Data Flow

每個 HTML 檔**完全 self-contained**（CSS + JS 都 inline，無共用 assets）。
這代表：改一個檔案不影響其他，但加 CSS token / 共用樣式時要 manually sync。

### 兩套 nav 風格

| 類型 | 應用 | 結構 |
|---|---|---|
| **內容頁 nav** | 12 個策略/技術頁 | `<header>` 含 `.nav-links`，list 12 個 page link |
| **Mockup banner** | 4 個 mockup 檔 | 頂部 `.mockup-banner` 單一「← 回 Mockup 列表」連結 |

### 關鍵 framing（已穩定，不要回頭混淆）

- **3 modes** = 依「誰用」（user role）分：A 員工 / B SMB IT / C Pro/MSP
- **Dashboard Builder = wedge product**（不是 Mode B 子功能）— 跨所有模式可用，藍海競爭
- **4 dimensions** = 用例維度：Deployment / Monitoring / Troubleshoot / Management
- 工程上 Dashboard Builder 仍是 **third skill class**（與 Diagnostic / Monitoring playbooks 並列），架構不變
- Marketing 上 Dashboard Builder **獨立成 wedge** 主推 — 詳見 dashboard-builder-product.html

## Conventions

### 設計系統 token

統一使用 CSS variables（每個檔案 `:root` 都有相同定義）：

```css
--bg-1: #0a1628;        /* base background */
--accent: #ff6b35;      /* 橘 · 主色 / Mode B */
--cyan: #00d9c5;        /* 青 / Mode A / links */
--purple: #a78bfa;      /* 紫 / Mode C */
--warn: #fbbf24;        /* 黃 / Wedge product (Dashboard Builder) */
--good: #10b981;        /* 綠 · ring 0 */
--bad: #ef4444;         /* 紅 · ring 2 */
```

### 顏色語義（嚴格遵守）

| 顏色 | 對應 | 例 |
|---|---|---|
| Cyan | Mode A · 員工 | employee-chat-mockup |
| Accent (橘) | Mode B · SMB IT · 主軸 | cockpit-mockup |
| Purple | Mode C · Pro/MSP | mode-c-pro-mockup |
| **Warn (黃)** | **Wedge product (Dashboard Builder)** | dashboard-builder-product / flow |

### 命名

- 品牌：**Network AI-Assistant** — `AI-Assistant` 部分用 `<span class="accent">` 標亮
- HTML 檔名：kebab-case
- 中英混用 OK，但對外面向（hero / titles）優先繁中

### Nav links 編輯時注意

- 大部分頁用 `<a class="nav-link muted-link" href="...">`（非 current 狀態）
- `architecture-v2-zh.html` / `architecture-v2.html` 例外用 `<a class="nav-link" href="...">`（無 muted-link）
- 縮排不一致：mockup-gallery 用 4 spaces，architecture 用 6 spaces
- 加新頁時要更新**所有 11 個內容頁** + index.html（mockup 不需更新 nav）

## Current Status

- ✅ 12 內容頁 + 4 mockup + sales deck 全部 live
- ✅ Dashboard Builder 已 reframe 為 wedge product
- ✅ EN / ZH 架構整合（一張 card + 頁內切換）
- ✅ 全部 nav 互通

### 🔜 Next Steps（無使用者明確指定，視需要）

- 真實 design partner 試用驗證 wedge thesis
- 客製 domain（取代 Vercel default）
- OG image / social preview meta tags
- 加入 Vercel Analytics（看流量）
- 補 Mode A 員工 chat 的更多 playbook 範例
- 將 freemium 定價放回（先前已移除 placeholder）

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
7. **加新頁要更新 nav 11 處 + index.html 3-4 處**（resource cards、files table、count）— 漏一處會不一致
8. **index.html 的 page count 出現在 3 個位置**：hero meta、resources section title、各種 narrative 文字
9. **不要把 mockup 加進 nav 12 link 列表** — mockup 只從 mockup-gallery 進入，不出現在內容頁 nav
10. **檔案列表表格用 `⇄` 符號**（U+21C4）標明 ZH ⇄ EN 兩個檔案是 mirror

## 詳細文件

- [README.md](README.md) — 給人看的功能介紹、檔案清單、使用情境
