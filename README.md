# 你的專業 AI 網管 · EnGenius Cloud AI Agent Skill Suite

> 把 EnGenius Cloud 整套 API 變成 AI 可動手做事的能力。
> 一個能跨多 org 看健康、查盲點、即時生 dashboard 的 AI 網管助理。

🔗 **Live demo**: https://network-ai-assistant.vercel.app
📍 **所有 URL 整理**：[`URLS.md`](./URLS.md)

> **狀態**：專案開發中，尚未正式 release。對外 OSS-facing 版的 README 草稿存在 [`README.oss-draft.md`](./README.oss-draft.md)，未來上 GitHub 公開時取代本檔即可。

## 📦 這包裝了什麼

一套搭配使用的 Claude Code skill bundle：

| | 內容 | 用途 |
|---|---|---|
| **[`dashboard-builder/`](./dashboard-builder/)** | dashboard-builder skill + 17 張 live dashboard + 12 widget + persona + design system | 動態組裝 AI 網管 dashboard |
| **[`api-skills/`](./api-skills/)** | RD 提供的 13 個 EnGenius Cloud data skill（hvs / networks / org-devices / troubleshoot…） | 打雲端 API 做實際讀寫操作 |

兩包搭配 = 完整的「你的專業 AI 網管」。Claude Code 透過 `/plugins install` 兩個 plugin 後即可使用。

## 🎯 主軸 · Dashboard Builder

**[`dashboard-builder/`](./dashboard-builder/)** — 整套 skill + 17 張 live dashboard + 完整 design system。

- **12 widgets** · **6 validated 情境** · **3 locales**（zh-TW / EN / JA）· **light + dark theme**
- 跑真實 EnGenius Cloud staging API · 雙 script workflow（refresh-all + compose.py）
- **AI 網管 persona**（[`skill/references/network-admin-persona.md`](./dashboard-builder/skill/references/network-admin-persona.md)）
- **Design System 守則**（[`skill/references/design.md`](./dashboard-builder/skill/references/design.md)）
- **Claude Code plugin**（可 `/plugins install`）

### 主入口

| URL | 用途 |
|---|---|
| **[`index.html`](./index.html)** | 主站首頁 · 直接帶進 dashboard-builder |
| **[`api-docs.html`](./api-docs.html)** | **互動式 API 文件（Swagger UI）** · 94 ops · 47 完整可試打 · 47 pending RD docs |
| **[`openapi.json`](./openapi.json)** | OpenAPI 3.1 spec · 自動從 `api-skills/skills/*/SKILL.md` 生成 |
| **[`dashboard-builder/architecture.html`](./dashboard-builder/architecture.html)** | ★ 主架構頁 · 你的 AI 專業網管定位 + 6 面向 + Roadmap + Appendix |
| **[`dashboard-builder/technical.html`](./dashboard-builder/technical.html)** | Technical Deep-Dive · widget / spec / compose / design system |
| **[`dashboard-builder/widget-catalog.html`](./dashboard-builder/widget-catalog.html)** | 12 widget spec viewer |
| **[`dashboard-builder/skill/`](./dashboard-builder/skill/)** | Skill 本體（SKILL.md + persona + design + compose.py） |

### 重新生 OpenAPI

```bash
# 改完 api-skills/skills/*/SKILL.md 後重跑這個一次：
python3 scripts/build-openapi.py
# → 重生 openapi.json，api-docs.html 自動讀新版
```

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

詳見 [`dashboard-builder/README.md`](./dashboard-builder/README.md) 跟 architecture.html。

## 📚 早期 Proposal 歷史檔案

[`proposal-archive/`](./proposal-archive/) — 2026-04 ~ 05 階段最初討論「AI 網管助理」proposal 的所有材料：

- 兩條產品線敘事（Mode A 員工 / Mode B SMB IT · Line 1 cloud-embedded / Line 2 skill-based）
- UI mockup（employee chat / cockpit / unified chat / dashboard-builder flow）
- 早期 Dashboard Builder 行銷頁（dashboard-builder-demo / implementation / prep）
- 互動式系統架構（architecture-v2 中英版）
- 早期 PoC（[`prototype/`](./proposal-archive/prototype/) · 連 staging API 跑通的舊版 dashboard）
- 早期 Line 2 對齊文件（[`docs/`](./proposal-archive/docs/) · widget-catalog.md / prompt-templates.md…）
- 10-slide pitch deck

入口：[`proposal-archive/index.html`](./proposal-archive/index.html)

> 已收斂為 dashboard-builder/，歷史檔案保留作脈絡參考。

## 📁 資料夾結構

```
network-ai-assistant/
├── index.html              ← 主站首頁（專業 AI 網管 entry）
├── api-docs.html           ← ★ 互動式 API 文件（Swagger UI 讀 openapi.json）
├── openapi.json            ← ★ OpenAPI 3.1 spec · 94 ops · auto-generated
├── README.md               ← 你正在看（內部狀態文件）
├── README.oss-draft.md     ← OSS release 用的對外版（release 時取代 README.md）
├── LICENSE                 ← MIT
├── CLAUDE.md               ← AI session 接手導讀
├── assets/                 ← 共用 logo / 架構圖
├── scripts/
│   ├── sync-refs.sh        ← 同步 persona/design.md → api-skills/references/
│   └── build-openapi.py    ← 從 api-skills/skills/*/SKILL.md 重生 openapi.json
├── dashboard-builder/      ← ★ 主軸：完整 skill + 17 張 dashboard + docs
│   ├── architecture.html
│   ├── widget-catalog.html
│   ├── *.html              ← 17 張 dashboard canvas
│   ├── skill/              ← SKILL.md + persona + design + compose.py（plugin-ready）
│   ├── live-data/          ← staging API snapshot
│   ├── scripts/            ← refresh-all.sh + build_topology.sh
│   └── docs/               ← persona-test-results / devlog / rd-handoff…
├── api-skills/             ← 🔌 RD 提供的 13 個 data skill（vendored）
│   ├── .claude-plugin/     ← plugin manifest（可 /plugins install）
│   ├── CLAUDE.md / 安裝說明.txt / requirements.txt
│   ├── references/         ← persona + design.md 鏡像（由 scripts/sync-refs.sh 同步）
│   ├── skills/             ← engenius-env / hvs / networks / org-{devices,licenses,backups,...}
│   │                         network-{ap,gateway,switch}-troubleshoot / team-members…
│   └── metadata/
└── proposal-archive/       ← 📚 早期 proposal 歷史檔案
    ├── index.html          ← 歷史檔案 hub（2-card chooser）
    ├── home-product.html / home-engineering.html
    ├── overview-pm-mkt.html / two-modes.html / use-case-matrix.html
    ├── system-diagram.html / architecture-v2-{zh,}.html
    ├── playbook-examples.html / blind-spots.html / pitch-deck.html
    ├── dashboard-builder-{demo,implementation,prep}.html
    ├── mockup-gallery.html + 4 *-mockup.html
    ├── prototype/          ← 早期 PoC（canvas / booth-hospitality / generated-log）
    └── docs/               ← 早期 Line 2 對齊文件
```

## 🔌 整合 RD 新 skill 的 workflow

每當 RD 給你新版 / 新 skill：

```bash
# 1) 把 RD 給的 skill 資料夾複製進 api-skills/skills/<name>/
#    （直接覆寫或新增）

# 2) 看變更
git diff --stat api-skills/

# 3) 本機測試（在 api-skills/ 下建 .venv，install requirements）
cd api-skills && uv venv && uv pip install -r requirements.txt && cd -

# 4) 確認 persona / design.md 是最新版同步過去
bash scripts/sync-refs.sh

# 5) commit
git add api-skills/
git commit -m "feat(api-skills): integrate <skill-name> from RD"
```

**Source-of-truth 規則**：
- `dashboard-builder/skill/references/{network-admin-persona,design}.md` = canonical
- `api-skills/references/` = mirror（每次 edit 完跑 `bash scripts/sync-refs.sh`）
- `.venv/` / `__pycache__/` / `.env*` 都已被 `.gitignore` 排除

## 🛠 技術細節

- **純靜態 HTML**：無 build 步驟、無 backend、無 framework
- **依賴**：僅 Google Fonts CDN（Inter / Noto Sans TC / JetBrains Mono）
- **離線可用**：CDN 不可達時也能基本顯示
- **互動**：所有 mockup / dashboard 純 vanilla JS 實作
- **部署**：Vercel auto-deploy（push to main → 30 秒內 live）

## 📐 設計系統

主站（`dashboard-builder/` + root index）用**深色 + warn 黃**（wedge product 色），主要色票：

- 底：深藍漸層 `#0a1628 → #0f1e3a`
- Wedge 強調：`#fbbf24`（Dashboard Builder 專屬）
- Accent：橘 `#ff6b35` · Cyan：`#00d9c5`

`proposal-archive/` 內保留原本雙 palette（淺色 marketing / 深色 engineering）的歷史脈絡，未調整。

詳細設計守則：[`dashboard-builder/skill/references/design.md`](./dashboard-builder/skill/references/design.md)

## 🚀 開發 / 維護

```bash
# 編輯檔案後
git add .
git commit -m "..."
git push
# Vercel 自動 redeploy ~30 秒內
```

架構細節與踩坑清單詳見 [`CLAUDE.md`](./CLAUDE.md)（給 AI session 接手用）。

## 📄 License

[MIT](./LICENSE) — 未來公開時自由使用、修改、商用、再散布。

## 🤖 AI 協作

This project was iteratively designed and built with Claude Code.
從 2026-04 早期 proposal 討論，到 2026-05 收斂為可安裝的 skill — 整個演化過程詳見
[`dashboard-builder/docs/devlog.md`](./dashboard-builder/docs/devlog.md)。
