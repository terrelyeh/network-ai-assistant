# CLAUDE.md — 你的專業 AI 網管 · EnGenius Cloud AI Agent Skill Suite

> Last updated: 2026-05-17（架構語言收斂 session · 完成 PR #9–#17）

## Project Overview

純靜態 HTML 站，主軸是 **「你的專業 AI 網管」** — 一套裝進 Claude Code 的 skill suite，把 EnGenius Cloud 整套 API 變成 AI agent 可動手做事的能力。

**核心定位**：不是 chatbot、不是 BI dashboard、不是 SaaS GUI、不是純「LLM + API」工具。是一個由 **skill primitives + 5 層知識架構（persona / design / house-rules / playbook / memory）** 組成的「**有 voice、有判斷、會記憶的 AI 同事**」。

完整功能與內容結構詳見 [README.md](README.md)。架構說明在 [`dashboard-builder/architecture.html`](dashboard-builder/architecture.html)。
**Live**: https://network-ai-assistant.vercel.app

## ★ 2026-05-17 架構語言收斂（這次 session 的重點）

**舊框架已棄用，新 session 不要再用**：

| 棄用的舊框架 | 現在用什麼 | 為什麼換 |
|---|---|---|
| 「Line 1 vs Line 2 兩條產品線」 | 統一「AI 專業網管」一條敘事 | Line 1 視覺 mockup 已歸入 archive、沒在推；維持二分法只會混淆 |
| 「Dashboard Builder is the wedge product」 | Skill suite where dashboard = 1/3 output modes（text / dashboard / action）| §06 reframed as proof points, not catalog |
| 「13 skills」（固定數字暗示封閉）| 「目前 13 skills, 持續擴增」（RD + AI 都能加新的）| 對齊「open evidence for infinite system」訊息 |
| 「house-rules.md = 品牌觀點 / 推薦邏輯」 | 「house-rules.md = EnGenius 平台規則與規範（事實層面）」 | 跟 persona 的「voice」混淆；house-rules 是 WHAT FACTS, persona 是 HOW |
| 「5 個 validated 情境」當作功能清單 | 「5 個 proof points 證明 AI 即時組裝跑得通」 | 跟「dashboard 都是即時組」punch line 矛盾 |
| 「3 層執行分工 / 5 層架構 / 2 條無法妥協原則」… 多套並存的舊 framework | 統一在 architecture.html §02 6 個面向 + §03 5 層深度說明 | 多 session 累積的疊床框架已合併 |

**所有 framing 的權威來源**：[`dashboard-builder/architecture.html`](dashboard-builder/architecture.html)（2026-05-17 完全重寫）。改任何對外用詞前先讀那一頁。

## Tech Stack

- **純靜態 HTML**（無 build / framework / backend），CSS + JS inline 每個檔自包
- **Vanilla JS** 所有互動 · **Google Fonts CDN**（Inter / Noto Sans TC / JetBrains Mono）
- **OpenAPI 3.1** 自動生成 + Swagger UI bundle from unpkg CDN
- **部署**：Vercel auto-deploy（push to main → 30s）
- **GitHub**：terrelyeh/network-ai-assistant
- **PoC 跑真 API**：Python 3 + `uv` venv + `requests`（用 vendored `api-skills/` skills）

## Directory Structure

```
network-ai-assistant/
├── index.html                       ★ 主站首頁（AI 專業網管 entry）
├── api-docs.html                    ★ 互動式 API 文件（Swagger UI 讀 openapi.json）
├── openapi.json                     ★ OpenAPI 3.1 spec · 94 ops · auto-generated
├── README.md / README.oss-draft.md  內部狀態 / OSS release 草稿
├── CLAUDE.md / URLS.md / LICENSE
├── assets/                          共用 logo / 架構圖
├── scripts/
│   ├── sync-refs.sh                 dashboard-builder/skill/references/ → api-skills/references/
│   └── build-openapi.py             從 api-skills/skills/*/SKILL.md 重生 openapi.json
│
├── dashboard-builder/               ★ 主軸 · v0.2
│   ├── architecture.html            ★ v6（2026-05-17 重寫）· 8 sections + 3 Appendix · 1800 行
│   ├── technical.html               Technical Deep-Dive（從 architecture 拆出）· widget / spec / compose / design system · 1900 行
│   ├── widget-catalog.html          12 widget spec viewer
│   ├── *.html                       17 張 dashboard canvas（5 情境 × 3 語言 + dark）
│   ├── live-data/*.json             refresh-all.sh 寫入的 staging snapshot
│   ├── skill/                       dashboard-builder skill（plugin-ready）
│   │   ├── SKILL.md / .claude-plugin/ / skills/dashboard-builder/（symlink）
│   │   ├── scripts/compose.py / runtime/runtime.js / theme/
│   │   ├── widgets/                 12 widget HTML partials
│   │   ├── references/              persona.md + design.md + 12 widget refs
│   │   └── examples/                6 validated spec JSON
│   ├── scripts/refresh-all.sh / build_topology.sh
│   ├── assets/shots/                gallery 用截圖
│   └── docs/                        persona-test-results / devlog / rd-handoff / rd-priorities / scenario-candidates / rd-meeting/
│
├── api-skills/                      🔌 RD 提供的 senao-api-skills（vendored）
│   ├── .claude-plugin/marketplace.json
│   ├── CLAUDE.md / 安裝說明.txt / requirements.txt
│   ├── references/                  persona + design.md 鏡像（sync-refs.sh 維護）
│   ├── skills/                      13 個 data skill（hvs / networks / org-* / team-members / network-{ap,gateway,switch}-troubleshoot / engenius-env / init-orgs）
│   └── metadata/
│
└── proposal-archive/                📚 早期 proposal 歷史檔案（不要動）
    ├── index.html                   archive hub
    ├── *.html / mockup/             早期內容頁、mockup、pitch-deck 等
    ├── prototype/                   舊版 PoC（2026-05-13 之前）
    └── docs/                        早期 Line 2 對齊文件
```

**Gitignore**：`api-skills/.venv/`、`__pycache__/`、`*.pyc`、`.env*`、`.vercel/`、`.playwright-cli/`

## Architecture & Data Flow

對外架構說明全部在 [`dashboard-builder/architecture.html`](dashboard-builder/architecture.html)，包含：

- §02 6 個專業面向（含架構圖：User → AI 諮詢 5 層知識 → Skill Primitives → 3 種 Output）
- §03 每一層深度說明（persona / design / house-rules / playbooks / memory 各一節，含具體範例）
- §04 AI 怎麼運作（即時組裝、不預寫）
- §05 Skill = 最小 primitive unit
- §06 Dashboard Output · 5 個 proof points
- §07 Roadmap · §08 Status
- Appendix A: Skills × Scenarios matrix · B: Glossary · C: Resources

**寫程式碼時要記住**：每個 HTML 檔 self-contained（CSS / JS inline），不共用 stylesheet。改視覺要找到具體哪個檔。

## Conventions

### 主站 palette（深色 · Wedge 黃）

```css
/* root index, api-docs, api-skills landing, dashboard-builder/* */
--bg-1: #0a1628;    --bg-2: #0f1e3a;
--accent: #ff6b35;  --cyan: #00d9c5;  --warn: #fbbf24;
```

`proposal-archive/` 內保留原本雙 palette（淺色 marketing + 深色 engineering），不再改動。

### 命名 / Brand

- 品牌：**Network AI-Assistant**（`AI-Assistant` 部分用 `<span class="accent">` 標亮）
- 檔名：kebab-case
- 新加 .html 頁要更新 index.html quicklink + URLS.md + README.md「主入口」表

## ★ openapi.json · Universal API Index（Claude Code 內外都用得上）

之前的誤解：「openapi.json 只給外部 AI / SDK generator 用」。**修正**：

| | Claude Code skill loader（runtime 引擎） | Claude Code AI（在跟使用者對話的我） |
|---|---|---|
| 讀什麼 | SKILL.md（為了 invoke skill） | **任何檔案** — 用 Read tool |
| 用 openapi.json 嗎？ | ❌ 不用（有自己的 skill schema） | ✅ **可以**，當作 universal API index |

**AI 在對話中用 openapi.json 的最佳場景**（比讀 13 個 SKILL.md + N 個 references/ 快很多）：

- **跨 skill 探索**：「找跟 license 相關的所有 op」→ 1 個 grep 搞定
- **快速寫 curl / 範例 code**：拿 method/path/auth header → 直接 output
- **schema 速查**：「`patch_general_policy_plus` 的 body 長怎樣」→ 1 個檔內找
- **Gap 分析**：「列所有 `x-rd-pending` 的 op」→ 1 個 jq query
- **跨 method filter**：「列出所有 GET / POST」→ openapi.json paths 結構直接 filter

**SKILL.md 才有的（openapi.json 沒有）**：persona / design 守則、flow modules、constraints、用法注意事項。

**所以兩個 source 是互補不是 parallel**：
- 要 invoke skill + 遵守 persona 規範 → SKILL.md 機制
- 要 cross-skill 查 / 快速 metadata 速查 → 讀 openapi.json

每次跑 `python3 scripts/build-openapi.py` 後 openapi.json 反映最新 SKILL.md — AI 查的永遠是最新版本。

## ★ Dashboard Builder Skill workflow

**雙 script workflow**（不打雲端 / 不生 HTML 兩個分工乾淨）：
```bash
bash dashboard-builder/scripts/refresh-all.sh                    # 撈 staging API → live-data/*.json（~14s）
python dashboard-builder/skill/scripts/compose.py \
  --spec dashboard-builder/skill/examples/<scenario>.spec.json \
  --out dashboard-builder/<name>.html \
  [--theme light|dark] [--locale en|ja]                          # spec JSON → 自包含 HTML（~200ms）
```

詳見 [`dashboard-builder/technical.html`](dashboard-builder/technical.html)。

### Plugin install / cache sync

`/plugins` → Add marketplace（指向 `api-skills/` 或 `dashboard-builder/skill/`）→ Install → User scope → **完全重啟 Claude Code**（不是 `/clear`）。

**改完 SKILL.md / persona / design.md 後**（Claude Code 不會自動 refresh）：
```bash
# 同步 plugin cache（最快）
SRC=dashboard-builder/skill
CACHE=~/.claude/plugins/cache/dashboard-builder/dashboard-builder/0.1.0
cp $SRC/SKILL.md $CACHE/
cp -R $SRC/references/* $CACHE/references/
cp $SRC/widgets/*.html $CACHE/widgets/
cp $SRC/scripts/*.py $CACHE/scripts/
# Or: /plugins → Uninstall + Reinstall（乾淨但慢）
```
→ 然後 `/clear` 或重啟 Claude Code 讓對話重新 load。

## ★ RD 給新 / 更新 skill 的 AI 處理 workflow

User 偏好「**不寫 import script，直接把 RD 給的內容丟給 AI 處理**」。流程：

1. **判斷範圍**：整包 / 單一 skill / 補 scripts / 全新 skill — 看路徑結構
2. **rsync 進來**，必須排除：
```bash
rsync -av --delete \
  --exclude='.venv/' --exclude='__pycache__/' --exclude='*.pyc' \
  --exclude='.claude/' --exclude='.env*' \
  --exclude='references/' \    # 保護我們的 persona/design.md 為 source-of-truth
  <user 給的路徑>/ ./api-skills/<目標位置>/
```
3. `git diff --stat api-skills/` 看變更
4. 提醒 user：`/plugins` Uninstall + Reinstall → **完全重啟 Claude Code**（不是 `/clear`）→ 試一個對話
5. **更新狀態文件**（很容易忘）：CLAUDE.md「⚠️ RD 端阻擋項目」、README 狀態表、`dashboard-builder/docs/rd-priorities.md`、`README.oss-draft.md` skill 清單
6. Commit + PR（branch: `update/api-skills-<簡述>` 或 `feat/api-skills-<新skill名>`）

## ⚠️ RD 端阻擋項目

**P0（解鎖 47 個 troubleshoot op）**：拿到 1 個關鍵資訊就解鎖大部分
- dolphin 的 URL pattern + 一個 working curl 範例（已驗證 14 種 path 全 404 — [`docs/rd-meeting/06-api-doc-questions.md`](dashboard-builder/docs/rd-meeting/06-api-doc-questions.md) Q1+Q2）
- subscribe 的 streaming protocol（或 polling 替代方案）— Q3+Q4

**P1（阻新 widget 類型）**：
- 沒有 history aggregation API → line_chart / sparkline / area_chart widget 沒法做
- 提議 endpoint shape 在 [`docs/rd-meeting/04-history-api-proposal.md`](dashboard-builder/docs/rd-meeting/04-history-api-proposal.md)

**自助工具 · OpenAPI gap 視覺化**：
- 跑 `python3 scripts/build-openapi.py` 自動掃 `api-skills/skills/*/SKILL.md` → 生 `openapi.json`
- `api-docs.html` 用 Swagger UI 渲染 → 47 個 `x-rd-pending` op 顯示為「⚠ TBD」— **這就是給 RD 看的 gap 報告**

完整優先序表：[`dashboard-builder/docs/rd-priorities.md`](dashboard-builder/docs/rd-priorities.md)

## Current Status

功能清單與 demo 細節詳見 [README.md](README.md) 跟 [`dashboard-builder/architecture.html`](dashboard-builder/architecture.html)（§08 Status 速覽表）。

### 🔜 Next Steps

**獨立可做（不等 RD）**：
1. **寫 `house-rules.md` v0** — 5 層知識架構最後 ready 拼圖。內容：EnGenius 平台**硬性規則與規範**（HVS 分數定義、license-device 綁定、plan 限制、設備支援矩陣、平台 quirks）。**注意 framing**：是事實層面，不是主觀建議。需 RD 整理 + 業務協助梳理
2. **`playbooks/{configure,monitor,troubleshoot}.md` v0** — Mental model 不是 script。Configure 跟 Monitor 可以先做（不卡 RD），Troubleshoot 等 RD 補 dolphin URL 後再寫
3. **新情境腦力激盪** — 走 validated path pipeline 加 examples/，可從 [`docs/scenario-candidates.md`](dashboard-builder/docs/scenario-candidates.md) 中 S8-S12 / N/T/M 系列挑

**Critical（仍卡 RD）**：
4. **拿到 dolphin URL + curl 範例** — unblock 47 個 pending op
5. **History aggregation API** — unblock 趨勢類 widget

**Pending（次優先）**：
- 日文版需 native speaker review（目前 LLM 草稿）
- `dashboard-builder/skill/` 整合進 `api-skills/skills/dashboard-builder/`（[`docs/rd-handoff.md`](dashboard-builder/docs/rd-handoff.md)）
- **Memory.md** — 等真實 SI 使用 1-2 個月後再實作（避免閉門造車）

## Common Pitfalls

### 一般 / Shell
1. **macOS sed 需 `-i ''`**
2. **每個 HTML 檔 self-contained** — sed across files 要全域；改視覺要找到具體哪個檔
3. **品牌字 `AI-Assistant` 才是 highlighted span**（不是 `Network`）
4. **新加 .html 頁要更新所有導引**：root `index.html` + `URLS.md` + `README.md` 主入口表

### API / Skill
5. **API key 千萬別 commit** — 永遠 export 到 env var
6. **api-skills/ 已 vendor 進 repo**（`.venv/` / `__pycache__/` / `.env*` 由 .gitignore 排除）
7. **viewer 角色 RBAC 限制**：能讀 network-level，不能讀 org-level（inventory / licenses）→ 測試用 Main_Org 或 Vertical Demo
8. **`get_inventory` / `get_licenses` 是 PRO plan only** — terrel org 因 BASIC 會回 402
9. **dolphin 是 Go service behind nginx** — 沒文件就 404，路徑不可能用猜的（已驗證 14 種 path）
10. **network-{ap,gateway,switch}-troubleshoot 3 個 skill 沒 scripts/**（subscribe / rpc 不能執行）

### Dashboard Builder
11. **Nested `<a>` 自動 auto-close** — 外+內都要 link 必須用 wrapper div 隔開
12. **spec 的 `compute_fns` 在 widget scripts 之後執行** — 因此 spec 可以 override 內建 computeFns（i18n 用這 trick）
13. **`compose.py` `deep_merge` 對 sections 用 id-based merge** — spec `locales[locale].sections` 可只列要 override 的 section
14. **Programmatic scroll 不會 fire scroll event**（preview tool 限制）— 用 IntersectionObserver 監聽 active 狀態
15. **dashboard-builder/ 跟 proposal-archive/prototype/ 不互通**：canvas 內 `live-data/` 是相對路徑

### Plugin / Persona / Design
16. **Plugin install 會 COPY 不是 symlink** — 改 SKILL.md / design.md 後 `~/.claude/plugins/cache/<plugin>/<version>/` 不會自動更新，要手動 sync 或 `/plugins` reinstall
17. **Plugin install 後要完全重啟 Claude Code**（不是 `/clear`）才會 re-scan
18. **SKILL.md MANDATORY 措辭 v3**：「session 首次必讀 · 後續可用 context · 但要透明說明」— 強制每次重讀 Claude 會違反規則
19. **persona / design.md 改動要 sync** — `bash scripts/sync-refs.sh` 把 dashboard-builder/skill/references/ → api-skills/references/，**source-of-truth 是前者**
20. **Worktree 路徑陷阱**：Write/Edit 用絕對路徑會寫到 main repo，不是 worktree → 用相對路徑
21. **dashboard-builder plugin 結構是 `skills/<n>/SKILL.md`** — Claude Code 不支援 SKILL.md at plugin root，要用 symlinks 回上層
22. **raw_html section 必須有 `raw_html_reason`** — `compose.py` 沒填會 warning，目的是累積 widget library 需求單
23. **Symlinks 在 git 跨平台**：macOS / Linux work，Windows checkout 會變一般檔（未來 RD 接手要注意）

### 架構語言（2026-05-17 新踩 · session 完了還會踩）
24. **不要再用「Line 1 / Line 2」框架** — 統一講「AI 專業網管」一條敘事
25. **不要說「13 skills」** — 用「目前 13 skills 持續擴增」或「目前的 skill suite」
26. **不要把 dashboards 講成「我們做的 5 個情境」** — 是「5 個 proof points 證明 pipeline 跑得通」
27. **house-rules.md ≠ 品牌觀點** — 是 EnGenius 平台硬性規則與規範（事實，不是主觀建議）
28. **改 architecture.html 章節 numbering 要同步改 TOC + top-nav** — 三個地方都要更新

## 詳細文件

### ⭐ 對外文件（架構說明 / 給 PMM partner）
- [`dashboard-builder/architecture.html`](dashboard-builder/architecture.html) ★ — 主架構 v6 · 8 sections + 3 Appendix · 含架構圖
- [`dashboard-builder/technical.html`](dashboard-builder/technical.html) — Technical Deep-Dive · widget / spec / compose / design system
- [`dashboard-builder/widget-catalog.html`](dashboard-builder/widget-catalog.html) — 12 widget spec viewer
- [`api-docs.html`](api-docs.html) + [`openapi.json`](openapi.json) — Swagger UI / OpenAPI spec
- [`URLS.md`](URLS.md) — 全站 URL 速查
- [`README.oss-draft.md`](README.oss-draft.md) — OSS release 用對外版本草稿（release 時 rename 取代 README.md）

### 核心 skill 文件（AI 載入用）
- [`dashboard-builder/skill/references/network-admin-persona.md`](dashboard-builder/skill/references/network-admin-persona.md) ★ Voice + escalation matrix
- [`dashboard-builder/skill/references/design.md`](dashboard-builder/skill/references/design.md) ★ Design System + 9 hard prohibitions
- [`dashboard-builder/skill/references/`](dashboard-builder/skill/references/) — 12 widget reference docs

### 開發 / 內部紀錄
- [`dashboard-builder/docs/scenario-candidates.md`](dashboard-builder/docs/scenario-candidates.md) — 12 個 scenario + 新菜色 N/T/M 系列
- [`dashboard-builder/docs/persona-test-results.md`](dashboard-builder/docs/persona-test-results.md) — 實測對話紀錄
- [`dashboard-builder/docs/devlog.{md,html}`](dashboard-builder/docs/) — AI 工具開發案例分享
- [`dashboard-builder/docs/rd-priorities.md`](dashboard-builder/docs/rd-priorities.md) — RD P0-P3 待補項目
- [`dashboard-builder/docs/rd-meeting/`](dashboard-builder/docs/rd-meeting/) — 6 份推 RD 會議材料（含 `06-api-doc-questions.md` 給 RD 的 10 題）

### 歷史檔案（不要動，已歸檔）
- [`proposal-archive/`](proposal-archive/) — 2026-04 ~ 05 早期 proposal 階段所有材料（2 條產品線敘事、mockup、舊 PoC、pitch deck、Line 2 對齊文件）
