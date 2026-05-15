# AI Demo Architecture

> Last updated: 2026-05-15
> Owner: PM/MKT (Lulu Yeh) · Implementation handoff: RD
> Scope: Line 2 — SKILL + AI Coding Agent + Dashboard Builder

## TL;DR（一句話）

> **Claude Code 在對話中編排 RD 的 13 個 data skill + 1 個 dashboard-builder skill，把真實 EnGenius Cloud 資料即時組成客製 dashboard。**

「即時組成」是 wedge——不是預先做好的模板，是訪客問問題的當下 AI 才決定 dashboard 長什麼樣。

---

## 兩個無法妥協的原則

1. **資料一定真實**——所有 dashboard 數字必須來自 staging API，不可硬編
2. **組裝一定即時**——dashboard 結構在對話中才決定，不可全套打包成 skill 預設出來

> 違反 1 → 觀眾識破是 mockup；違反 2 → 變成普通 SaaS 預設 view，wedge 故事死

---

## 5 層架構

```
┌──────────────────────────────────────────────────────────────────────┐
│  L5 · 操作員 + 訪客（人）                                            │
│  booth presenter / hospitality vertical visitor / partner            │
└──────────────────────────────▲───────────────────────────────────────┘
                               │ 自然語言
┌──────────────────────────────┴───────────────────────────────────────┐
│  L4 · Claude Code（orchestrator）                                    │
│  - 從對話讀意圖                                                       │
│  - 選哪些 data skill 要呼叫                                          │
│  - 寫 dashboard spec JSON                                            │
│  - 呼叫 dashboard-builder.compose                                    │
│  - append manifest entry                                             │
└──────────────────────────────▲───────────────────────────────────────┘
                               │ python scripts/call_api.py ...
                               │ python scripts/compose.py ...
┌──────────────────────────────┴───────────────────────────────────────┐
│  L3 · Skills 層（RD 擁有）                                            │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐    │
│  │ 13 個 DATA SKILL（讀寫 API）│  │ 1 個 DASHBOARD-BUILDER (新) │    │
│  │ • init-orgs    • org-licenses│  │ • theme/tokens + base.css   │    │
│  │ • hvs          • org-backups │  │ • widgets/  (8 個元件)      │    │
│  │ • networks     • org-grps    │  │ • compose.py                │    │
│  │ • org-devices  • org-tmpls   │  │ • references/widget_*.md    │    │
│  │ • team-members • engenius-env│  │                             │    │
│  │ • network-ap/gw/sw-trbl 🔴   │  │                             │    │
│  └─────────────────────────────┘  └─────────────────────────────┘    │
└──────────────────────────────▲───────────────────────────────────────┘
                               │ HTTPS + bearer token
┌──────────────────────────────┴───────────────────────────────────────┐
│  L2 · EnGenius Cloud（RD 擁有，已存在）                              │
│  falcon.staging.engenius.ai / Dolphin 平台 / Cloud GUI               │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│  L1 · Browser + Filesystem（觀眾看到的東西）                          │
│  prototype/live-data/*.json   ← Claude 寫，dashboard 讀              │
│  prototype/canvas-*.html      ← Claude compose 出來                  │
│  prototype/generated-log.html ← 每生一張，這裡跳一條 log             │
│  static HTTP server (autoPort) → browser preview                     │
│  HTML 內建 setInterval 5s poll                                       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 各層職責

| 層 | 誰擁有 | 主要負責 |
|---|---|---|
| L5 操作員 | 你（booth team） | 跟訪客互動、引導對話節奏、處理意外 |
| L4 Claude Code | Anthropic（runtime） | 對話理解、skill 編排、生 spec、呼叫 builder |
| L3 Data Skills | RD | 包裝 cloud API、處理識別解析、寫入 schema 守護 |
| L3 Dashboard Builder | RD（接手） | widget 視覺一致性、合成 HTML、live-data 綁定 |
| L2 Cloud | RD | API 穩定、staging 資料完整、權限模型 |
| L1 Artifacts | Claude 寫 / RD 規範 | 檔案結構約定、poll mechanism、log spec |

---

## Dashboard Builder Skill 內部結構

```
api-skills/skills/dashboard-builder/      ← 目標位置（RD 整合後）
prototype/dashboard-builder-skill/         ← 目前 prototype 位置
│
├── SKILL.md                               ← 文件 + Flow Modules
├── scripts/
│   └── compose.py                         ← 主入口：spec JSON → canvas HTML
├── theme/
│   ├── tokens.css                         ← 顏色、字體、spacing
│   └── base.css                           ← shell layout、sticky header、footer
├── widgets/                               ← 每個 widget = HTML partial + JS module
│   ├── alert.html
│   ├── kpi_grid.html
│   ├── card.html                          ← wrapper（標題+meta+chips）
│   ├── table.html                         ← 含 filter chips + row expand
│   ├── bar_list.html
│   ├── chip_strip.html                    ← 空 network 標籤
│   ├── topology_tree.html
│   └── footer.html
├── runtime/
│   └── runtime.js                         ← poll mechanism + widget registry + event bus
└── references/                            ← 給 Claude 看的 widget 規格
    ├── widget_alert.md
    ├── widget_kpi_grid.md
    ├── widget_table.md
    └── ...
```

### Dashboard spec JSON 範例

Claude 在對話中產出這份 spec，呼叫 `compose.py` 就會渲染：

```json
{
  "title": "Main_Org 健康總覽",
  "subtitle": "EnGenius Cloud Staging · org_id: 5e410f44...",
  "live_data": {
    "inventory": "live-data/inventory.json",
    "memberships": "live-data/memberships.json",
    "topology": "live-data/topology.json"
  },
  "sections": [
    {
      "widget": "alert",
      "id": "license-crit",
      "severity": "critical",
      "title": "License 全面過期警示",
      "body_compute": "license_summary"
    },
    {
      "widget": "kpi_grid",
      "items": [
        {"label": "Devices", "value_path": "inventory.device_candidates.length", "clickable": {"target": "device-fleet"}},
        {"label": "License Expired", "severity": "critical", "value_compute": "expired_count"},
        {"label": "Active Networks", "severity": "warning", "value_compute": "active_networks_ratio"},
        {"label": "Team Members", "value_path": "memberships.org_member_candidates.length"}
      ]
    },
    {
      "widget": "table",
      "id": "device-fleet",
      "title": "Device Fleet",
      "data_source": "inventory.device_candidates",
      "filters": [
        {"label": "All", "filter": "all"},
        {"label": "AP", "filter": "type:ap"},
        {"label": "Switch", "filter": "type:switch"},
        {"label": "Expired only", "filter": "license_status:expired"}
      ],
      "columns": [...],
      "expandable_rows": true
    },
    {
      "widget": "topology_tree",
      "id": "topology",
      "data_source": "topology.orgs",
      "auto_expand": "richest_org"
    }
  ]
}
```

---

## Booth Demo Workflow（90 秒主秀）

```
[展前 5 分鐘]
  操作員：./prototype/scripts/refresh-all.sh
  → 重撈所有 6 個 JSON 到 live-data/
  → 確認資料新鮮

[訪客抵達]
  訪客：「我管 5 個客戶的網路，能幫我看一下總體狀況嗎？」

[15 秒]
  操作員 → Claude Code:「幫我撈所有 org 的 device + license + member」
  Claude：runs 5 個 skill 並行 → 寫入 live-data/*.json
  Claude：「Main_Org 有 10 台設備、全 license expired，要不要先看這個？」

[30 秒]
  訪客點頭
  操作員 → Claude:「對，做一張 dashboard 從『健康』角度看 Main_Org」
  Claude：寫 dashboard spec → 呼叫 dashboard-builder.compose →
          產出 canvas-org-health-<TS>.html
  操作員：開 browser preview

[20 秒]
  訪客瀏覽 dashboard
  訪客：「我想看跨 5 個 org 的關係」

[25 秒]
  操作員 → Claude:「加一個 topology 區塊」
  Claude：跑 topology aggregate 腳本 → 修改 spec、append section →
          重新 compose
  ← 觀眾看到 dashboard 在他眼前長出新區塊（核心 wow）

[彩蛋 15 秒]
  訪客：「Front Desk 已經 5 年沒登入了還有 7 個 network 權限？」
  操作員 → Claude:「列出可疑成員」
  Claude：highlight 那幾筆 → 建議下一步操作（不執行寫入）
```

---

## 為什麼這個架構成立

### 對 RD 友善
- Data skills 已有，不需改既有 13 個 skill
- 只需新增 1 個 dashboard-builder skill
- Widget 視覺集中在一處，UI 升級不影響資料層

### 對 Claude 友善
- 不用每張 dashboard 手刻 HTML / CSS（700 行）
- 只需產 spec JSON（30-80 行）
- 視覺一致性由 builder 保證

### 對觀眾友善
- 真實資料（無 fake data tells）
- bespoke 組合（不像預設模板）
- 即時長出（看得到 AI 在思考）

### 對你（PM/MKT）友善
- Widget 視覺改一次，所有未來情境自動升級
- 加新情境不用改 builder skill，只要 Claude 對話中組
- Demo 失敗 fallback = 開冷凍版 canvas（HTML + JSON 都在）

---

## 現況 vs Roadmap

| 元件 | 狀態 | 備註 |
|---|---|---|
| L2 Cloud | ✅ 上 | staging 可用 |
| L3 data skills × 10 | ✅ 可跑 | ~46 個 op 可呼叫 |
| L3 troubleshoot × 3 | 🔴 規劃中 | 47 個 op 沒 script |
| L3 dashboard-builder | 🟡 **本次任務** | prototype 中 |
| L4 Claude Code | ✅ | 已能跑 |
| L1 canvas + live-data | ✅ 5 個 canvas 已 work | 自動 poll 已驗證 |
| L1 manifest log | ✅ | generated-log.html 已 work |
| L5 booth playbook | ✅ | `docs/booth-presenter-cheatsheet.md` |
| 一鍵 refresh 腳本 | 🟡 | 需補 `refresh-all.sh` |

---

## 接下來要驗證的事

1. **拆 widget 後視覺/互動跟原 v1 canvas 完全一致**（功能 parity）
2. **再做 1 個情境驗證 widget 真的可重用**（例如 S4 離職員工 / S5 license 預警）
3. **改一次 widget 樣式，所有 canvas 自動套用**（design uplift 流程）
4. **跟 RD 對齊 dashboard-builder 整合進 api-skills 的時程**
