# 你的專業 AI 網管

**EnGenius Cloud AI Agent Skill Suite — Your professional AI network admin, powered by Claude Code.**

把 EnGenius Cloud 整套 API 變成 AI 可動手做事的能力 — 一個能跨多 org 看健康、查盲點、即時生 dashboard 的 AI 網管助理。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-ff6b35.svg)](https://claude.com/claude-code)
[![Live Demo](https://img.shields.io/badge/Live-Demo-00d9c5.svg)](https://network-ai-assistant.vercel.app)

🔗 **Live demo / 視覺說明**: https://network-ai-assistant.vercel.app

---

## 🎯 這是什麼

一個給 Claude Code 用的 **Skill 套件**，讓 AI 可以：

- 🔍 **跨多個 EnGenius Cloud organization 看健康狀態** — HVS 分數、設備數、licenses、alerts
- 🩺 **診斷 AP / Switch / Gateway 問題** — client list、cable diag、event log、即時 LED 指示
- 📊 **依情境動態組 dashboard** — 你問問題、AI 即時把資料組成可看的視覺
- 🔐 **稽核權限與設定** — 離職人員權限檢查、跨 org 設備調撥、license 到期 timeline
- 🌏 **三語言介面** — zh-TW / English / 日本語，light + dark theme

不是另一個獨立 app — 是裝進 Claude Code 後，你直接用對話讓 AI 幫你管網路。

## 🔧 兩個搭配使用的 Skill bundle

| Bundle | 角色 | 內容 |
|---|---|---|
| **[`api-skills/`](./api-skills/)** | 打雲端 API | 13 個 data skill（hvs / networks / org-devices / org-licenses / troubleshoot…） |
| **[`dashboard-builder/`](./dashboard-builder/)** | 組視覺 | 12 widget + 6 validated 情境 + persona + design system |

兩個都裝進 Claude Code = 完整的 AI 網管助理。

## ✨ 你可以做到什麼

實際對話範例（直接打給 Claude Code 就行）：

```
你：幫我看一下 Vertical Demo 這個 org 的健康狀態
AI：[抓 HVS + inventory + alerts]
    [組成 org-health dashboard，含 KPI / device 分布 / alert timeline]
    HVS 分數 87/100，有 3 台 AP offline 超過 24 小時，請優先處理。
```

```
你：Ann 離職了，幫我看一下他在所有 org 還有什麼權限
AI：[跨 org 跑 team-members + role]
    [組 offboarding-audit dashboard]
    Ann 在 5 個 org 還是 admin，列出來給你 — 點選擇要 revoke 哪些。
```

```
你：哪些 license 下個月要到期？
AI：[跨 org 跑 org-licenses]
    [組 license-renewal timeline + cost summary]
    7 個 license 30 天內到期，總續約成本 USD 2,340。
```

```
你：客戶說 AP-LAB-03 連不上 SSID，幫我看一下
AI：[抓 client list + event log + cable diag]
    [組 ad-hoc troubleshoot dashboard]
    Radio 2.4G channel 1 過載（鄰居 AP 太多），建議切到 channel 11。
```

更多範例：[`dashboard-builder/docs/persona-test-results.md`](./dashboard-builder/docs/persona-test-results.md)

## 🚀 Quick Start

### 前置需求

- **Claude Code CLI** — https://docs.claude.com/claude-code（已登入帳號）
- **Python 3.10+** — `python3 --version` 確認
- **EnGenius Cloud 帳號 + API Key** — 從 https://cloud.engenius.ai 取得

### 步驟 1 · 下載這個 repo

```bash
git clone https://github.com/<your-username>/network-ai-assistant.git
cd network-ai-assistant
```

### 步驟 2 · 安裝兩個 plugin 到 Claude Code

在 Claude Code 對話框輸入 `/plugins`，然後：

1. **Manage marketplaces → Add marketplace** — 輸入你本機 repo 路徑兩次：
   - 一次指向 `<path>/network-ai-assistant/api-skills/`
   - 一次指向 `<path>/network-ai-assistant/dashboard-builder/skill/`
2. **Install plugin** — 在清單中分別找到 `senao-api-skills` 跟 `dashboard-builder`，都選擇 **User scope** 安裝
3. **重啟 Claude Code**（完全 quit 重開，不是 `/clear`）

### 步驟 3 · 設定 EnGenius 環境與 API Key

在 Claude Code 對話框打：

```
切到 staging
```

AI 會問你環境（dev / staging / prod）跟 API Key，輸入後會寫進 `~/.claude/engenius_env.json`，之後不用重設。

### 步驟 4 · 開始用

```
列出我有權限的所有 org
```

```
跑一下 Main_Org 的健康檢查
```

```
跨 org 看誰的 license 30 天內到期
```

完成 ✅

## 📂 資料夾結構

```
network-ai-assistant/
├── README.md                ← 你正在看
├── LICENSE                  ← MIT
├── CLAUDE.md                ← AI session 接手用內部狀態
├── index.html               ← Live demo 入口頁
├── assets/                  ← 共用 logo / 架構圖
├── scripts/
│   └── sync-refs.sh         ← 同步 persona/design.md 到 api-skills/
│
├── api-skills/              ★ Bundle 1: 打雲端的 13 個 data skill
│   ├── .claude-plugin/      ← Claude Code plugin manifest
│   ├── skills/              ← engenius-env / hvs / networks / org-* / troubleshoot…
│   ├── references/          ← persona + design.md（mirror）
│   └── 安裝說明.txt          ← RD 原始安裝說明
│
├── dashboard-builder/       ★ Bundle 2: 組視覺的 skill + 17 張 demo dashboard
│   ├── architecture.html    ← 完整架構說明
│   ├── widget-catalog.html  ← 12 widget spec viewer
│   ├── *.html               ← 17 張 live dashboard demo
│   ├── skill/               ← Claude Code plugin（SKILL.md + compose.py + widgets）
│   ├── live-data/           ← Staging API snapshot
│   ├── scripts/             ← refresh-all.sh + build_topology.sh
│   └── docs/                ← persona test / devlog / RD handoff
│
└── proposal-archive/        📚 早期 proposal 階段歷史檔案（2026-04 ~ 05）
```

## 🧩 功能完整清單

### `api-skills/` — 13 個 data skill

| Skill | 能做什麼 |
|---|---|
| `engenius-env` | 切換 dev / staging / prod 環境、管理 API key |
| `init-orgs` | 列出帳號有權限的所有 org |
| `hvs` | 抓 Health View Score（每個 org 的健康分數） |
| `networks` | 列出 org 內的 networks、查 network 設定 |
| `org-devices` | 列出 / 查詢 org 內所有設備（AP / Switch / Gateway） |
| `org-licenses` | 查 license 狀態 / 到期日 / key |
| `org-backups` | 查 config backup 歷史 |
| `org-network-groups` | 管理 network 分組 |
| `org-network-templates` | Network template 操作 |
| `team-members` | 查詢 / 管理 org 成員與權限 |
| `metadata` | API metadata 查詢 |
| `network-ap-troubleshoot` | AP 診斷（client list / event log / cable diag）⚠️ scripts 待補 |
| `network-gateway-troubleshoot` | Gateway 診斷 ⚠️ scripts 待補 |
| `network-switch-troubleshoot` | Switch 診斷 ⚠️ scripts 待補 |

### `dashboard-builder/` — 12 widget

`alert` · `kpi_grid` · `table` · `bar_list` · `stacked_bar_list` · `donut` · `gauge` · `pivot_table` · `chip_strip` · `topology_tree` · `timeline` · `heatmap`

完整 spec：[`dashboard-builder/widget-catalog.html`](./dashboard-builder/widget-catalog.html)

### 已 validated 的 6 個情境

- **S2 Multi-Org Governance** — MSP partner 跨 5 個 org 治理
- **S3 Org Health** — 單一 org 健康總覽（HVS / 設備 / alerts）
- **S4 Offboarding Audit** — SOC2 視角的離職權限稽核
- **S5 License Renewal** — 跨 org license 到期 timeline
- **S7 Cross-Org Reallocation** — 跨 org 設備調撥規劃
- **Org Device Distribution** — 設備類型分布

每個情境都有 3 語言版（zh-TW / EN / JA），可在 [Live demo](https://network-ai-assistant.vercel.app) 看。

## 🏗 架構概念

```
你的問題（自然語言）
        ↓
   Claude Code
        ↓
   ┌────────────┴─────────────┐
   ▼                          ▼
api-skills/                dashboard-builder/
（打雲端 API）              （把結果組成視覺）
   │                          │
   ▼                          ▼
EnGenius Cloud API     HTML dashboard（self-contained）
```

詳細架構：[`dashboard-builder/architecture.html`](./dashboard-builder/architecture.html)（含 §00 產品全貌 / §02c Persona / §03f Design System / §04b Demo Readiness）

## 🌐 Live Demo

不想裝？先看 [https://network-ai-assistant.vercel.app](https://network-ai-assistant.vercel.app) — 純前端展示所有 17 張 dashboard、widget catalog、架構說明。資料是真實 staging API snapshot（已脫敏）。

## 🛠 進階：為這個 repo 貢獻

### 改 persona / design.md

```bash
# 編輯 source（單一 source-of-truth）
vim dashboard-builder/skill/references/network-admin-persona.md
vim dashboard-builder/skill/references/design.md

# 同步到 api-skills/ mirror
bash scripts/sync-refs.sh
```

### 整合 RD 給的新 skill

```bash
# 1) 把 RD 給的 skill 資料夾覆寫進 api-skills/skills/<name>/
# 2) git diff 看變更
# 3) cd api-skills && uv venv && uv pip install -r requirements.txt
# 4) 本機 Claude Code 重新 install plugin 測試
# 5) 沒問題就 git commit
```

### 用 dashboard-builder 組新 dashboard

```bash
# 撈最新 staging 資料
bash dashboard-builder/scripts/refresh-all.sh

# Spec JSON → 自包含 HTML
python dashboard-builder/skill/scripts/compose.py \
  --spec dashboard-builder/skill/examples/<scenario>.spec.json \
  --out dashboard-builder/<name>.html \
  [--theme light|dark] [--locale en|ja]
```

更詳細的開發內幕、設計決策、踩坑紀錄 → [`CLAUDE.md`](./CLAUDE.md)

## 📋 目前狀態

| 區塊 | 狀態 |
|---|---|
| `api-skills/` 13 個 data skill | ✅ 10 個完整 / ⚠️ 3 個 troubleshoot 缺 scripts（RD 待補） |
| `dashboard-builder/` 12 widget | ✅ 全部完成 |
| 6 個 validated 情境 | ✅ 全部過 staging 測試 |
| 3 語言 + dark theme | ✅ zh-TW / EN / JA（日文需 native review） |
| Claude Code plugin install | ✅ 兩個 bundle 都可 `/plugins install` |
| 歷史 aggregation API | 🟡 RD 待補（解鎖 line_chart / sparkline widget） |

詳細待辦：[`dashboard-builder/docs/rd-priorities.md`](./dashboard-builder/docs/rd-priorities.md)

## 🤝 貢獻

歡迎發 issue 或 PR。回報 bug 時請帶上：

- Claude Code 版本（`claude --version`）
- Python 版本
- 你跟 AI 的對話（哪句話讓事情壞掉）
- AI 回的錯誤訊息

## 📄 License

[MIT License](./LICENSE) — 你可以自由使用、修改、商用、再散布。

## 🙏 致謝

- **EnGenius Cloud RD team** — 提供 [`api-skills/`](./api-skills/) 內全部 13 個 data skill
- **Anthropic Claude Code** — 整套產品建立在 Claude Code 的 plugin 機制之上
- 完整開發歷程（從 proposal 到 skill）：[`dashboard-builder/docs/devlog.md`](./dashboard-builder/docs/devlog.md)
