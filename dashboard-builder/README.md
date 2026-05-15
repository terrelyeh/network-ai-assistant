# Dashboard Builder · AI Demo · v1

> Self-contained 區，包含 2026-05-15 → 16 session 設計的所有 AI demo 內容
> 不跟 root 或 `prototype/` 之前的東西混

## Entry points

| URL | 用途 |
|---|---|
| **[architecture.html](architecture.html)** | 主入口 · 完整架構說明 + dashboard gallery + RD 動作項 |
| **[widget-catalog.html](widget-catalog.html)** | 10 個 widget 的 markdown spec viewer |

## 7 個 dashboard canvases（live, 5 秒 poll real staging API）

| 檔案 | 情境 |
|---|---|
| [org-health.html](org-health.html) | S3 · Main_Org 健康總覽（skill-composed v2，主秀） |
| [org-health-v1.html](org-health-v1.html) | S3 · 同上的 hand-crafted v1（比對用） |
| [org-health-dark.html](org-health-dark.html) | S3 · dark theme variant 示範 |
| [offboarding-audit.html](offboarding-audit.html) | S4 · SOC2 視角的離職權限稽核 |
| [license-renewal.html](license-renewal.html) | S5 · 跨 org license 到期 timeline |
| [multi-org-governance.html](multi-org-governance.html) | S2 · MSP partner 跨 5 個 org 治理 |
| [cross-org-reallocation.html](cross-org-reallocation.html) | S7 · 跨 org 設備調撥規劃（gauge + heatmap） |

## 資料夾結構

```
dashboard-builder/
├── README.md                ← 你正在看
├── architecture.html        ← 主說明頁
├── widget-catalog.html      ← Widget spec viewer
├── *.html                   ← 7 張 canvas dashboard
├── live-data/               ← 真實 staging API snapshot
├── skill/                   ← dashboard-builder skill（待 RD 接手）
│   ├── SKILL.md
│   ├── scripts/compose.py
│   ├── theme/{tokens,base,tokens-dark}.css
│   ├── widgets/             ← 10 個 widget HTML partial
│   ├── runtime/runtime.js
│   ├── references/          ← 10 個 widget spec markdown
│   └── examples/            ← 6 份 spec JSON
├── scripts/                 ← Helper bash
│   ├── refresh-all.sh       ← 一鍵刷新所有 live-data
│   └── build_topology.sh    ← 跨 org topology 聚合
├── assets/shots/            ← Gallery 用截圖
└── docs/
    ├── architecture.md      ← 5 層架構文件
    ├── rd-handoff.md        ← dashboard-builder 整合進 api-skills 的步驟
    ├── rd-priorities.md     ← RD P0-P3 待補項目
    ├── scenario-candidates.md ← 10 個情境腦力激盪
    └── rd-meeting/          ← 推進 P0 troubleshoot scripts 的 4 份材料
```

## 怎麼使用

### 看 demo
```
open dashboard-builder/architecture.html
```

### 在展會前 5 分鐘刷新資料
```
bash dashboard-builder/scripts/refresh-all.sh   # 約 14 秒
```

### 用 spec 生新 dashboard
```
python dashboard-builder/skill/scripts/compose.py \
  --spec dashboard-builder/skill/examples/org-health.spec.json \
  --out dashboard-builder/new-dashboard.html

# 切 dark mode
python dashboard-builder/skill/scripts/compose.py \
  --spec ... \
  --out ... \
  --theme dark
```

## 跟 root 的 prototype/ 是什麼關係？

| | `prototype/` | `dashboard-builder/` |
|---|---|---|
| 內容 | 2026-05-13 之前的 PoC（canvas.html / canvas-network-audit.html / etc.）+ booth-hospitality 演練檔 + generated-log/manifest | 2026-05-15 ~ 16 session 的所有 AI demo 內容 |
| 用 widget 化架構嗎 | 否（每張 canvas 手刻 HTML） | 是（10 widget + spec JSON 組合） |
| 待 RD 接手 | 否 | skill/ 子資料夾 |

兩邊獨立、互不依賴。

## See also

- `CLAUDE.md`（root）— 整個 repo 的 session 起手導讀
- `prototype/`（root sibling）— 舊版 PoC 檔
