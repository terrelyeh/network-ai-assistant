# Handoff: dashboard-builder skill → api-skills/

> 對象：RD（Backend/Skills team）
> 來源：`prototype/dashboard-builder-skill/`（PM/MKT prototype）
> 目標：`api-skills/skills/dashboard-builder/`（與其他 13 個 RD skill 並列）
> 預估整合時間：1-2 個工作天
> Last updated: 2026-05-16

## TL;DR

PMM 在 prototype 階段做了一個新 skill — `dashboard-builder` — 把資料（其他 skill 撈到的 JSON）+ 一份 spec JSON 組成一張互動式 HTML dashboard。**邏輯已驗證**（5 個情境跑過、8 個 widget 已 work），現在請 RD：

1. **整合進 `api-skills/skills/dashboard-builder/`**，跟其他 skill 並列
2. **檢查 / 補齊**規格不夠完整的地方（C* constraints、補 references/widget_*.md 對齊風格）
3. **加進 plugin metadata**（讓 Claude Code 知道有這個 skill 可用）
4. **長期維護**：widget 美感升級、新增 widget、theme variant、跨 org 資料聚合 helper

## Current location

```
prototype/dashboard-builder-skill/
├── SKILL.md                              ← 文件 + Flow Modules（已比照 RD 既有 SKILL.md 風格）
├── scripts/compose.py                    ← 主入口（170 行）
├── theme/
│   ├── tokens.css                        ← 設計變數
│   └── base.css                          ← shell layout
├── widgets/                              ← 8 個 widget HTML partial
│   ├── alert.html
│   ├── kpi_grid.html
│   ├── table.html
│   ├── bar_list.html
│   ├── donut.html
│   ├── chip_strip.html
│   ├── topology_tree.html
│   └── timeline.html
├── runtime/runtime.js                    ← poll mechanism + widget registry + event bus
├── references/                           ← 9 份 markdown
│   ├── index.md
│   └── widget_<name>.md × 8
└── examples/                             ← 5 份驗證過的 spec
    ├── org-health.spec.json
    ├── off-boarding-audit.spec.json
    ├── license-renewal.spec.json
    └── multi-org-governance.spec.json
```

## Target location

```
api-skills/skills/dashboard-builder/         ← 跟 13 個 RD skill 並列
├── SKILL.md
├── scripts/
│   └── call_api.py                          ⚠ 跟其他 skill 命名統一（但內部是 compose.py 邏輯）
├── theme/
├── widgets/
├── runtime/
├── references/
└── examples/
```

或者，因為這個 skill 不是「呼叫 cloud API」，是「render HTML」，可考慮另開資料夾：

```
api-skills/skills/dashboard-builder/
├── SKILL.md
├── scripts/
│   └── compose.py                           ✓ 保留原名（dashboard-builder ≠ API caller）
└── ...
```

**請 RD 決定**：(a) 統一檔名為 `call_api.py`、(b) 另開命名規則允許 `compose.py`。

## 為什麼有這個 skill

詳見 [architecture-demo.html](../architecture-demo.html)，核心 wedge：

> Claude Code 在對話中編排 RD 的 13 個 data skill + 1 個 dashboard-builder skill，把真實資料即時組成客製 dashboard。「**即時組成**」是賣點——不是預先做好的模板。

目前所有 demo 都是 PMM 手刻 700+ 行 HTML。Skill 化後：
- Claude 只要寫 ~150 行 spec JSON
- 視覺一致性由 widget library 保證
- 加新情境不用改 widget 程式碼
- RD 可以單獨美化 widget，所有 dashboard 自動升級

## 整合步驟

### Step 1 — 複製檔案

```bash
cp -r prototype/dashboard-builder-skill/* api-skills/skills/dashboard-builder/
```

注意：`api-skills/` 是 gitignored（屬於 RD 套件），複製進去後在 RD 的 release flow 裡 commit。

### Step 2 — 對齊 SKILL.md 風格

現有 SKILL.md 已比照 `networks/SKILL.md` 風格（含 frontmatter / Flow Modules / Constraints）。RD 可能想：

- 補 description 中的「invoke trigger phrases」
- 把 Flow Modules F0-F3 拆得跟其他 skill 一致
- 補 C7-C10 constraints（如果有跨 skill 一致要求）

### Step 3 — 驗證 examples 跑得通

```bash
cd api-skills
source .venv/bin/activate
export MANAGE_SYSTEM_URL="https://falcon.staging.engenius.ai"
export API_KEY="<your key>"

# Refresh data
python skills/init-orgs/scripts/call_api.py --operation-id get_user_orgs > /tmp/orgs.json
# ... 其他 skill ...

# Compose dashboard
python skills/dashboard-builder/scripts/compose.py \
  --spec skills/dashboard-builder/examples/org-health.spec.json \
  --out /tmp/canvas-test.html

# 開瀏覽器看效果
open /tmp/canvas-test.html
```

⚠ Compose 之前要把 live-data/*.json 放在 canvas 旁邊（同層 `live-data/` 資料夾），HTML 才 fetch 得到。Prototype 用 `prototype/live-data/`；整合時看 RD 想怎麼定 path 規範。

### Step 4 — 加進 plugin metadata

`.claude/plugins/` 或 `metadata/` 那邊登錄 dashboard-builder skill 的 capability，讓 Claude Code SDK 知道。

### Step 5 — 驗證 5 個情境

執行 `examples/*.spec.json` 全部 5 個（含本次新增的 multi-org-governance），確認：

- [ ] alert / kpi / table / bar_list / donut / chip_strip / topology_tree / timeline 都正常 render
- [ ] cross-widget interactions work（topology tree 點 device → table 自動 expand）
- [ ] auto-poll 5 秒 work（修改 live-data 後 dashboard 自動 reflect）
- [ ] Refresh button work
- [ ] 跨 5 個 spec 視覺一致（同一份 theme token 套用所有）

## 可改進 / nice-to-have

依優先序：

| 優先 | 改進 | 影響 |
|---|---|---|
| P0 | 路徑 `live-data/` 變可配置（spec 內可以指定） | 多 dashboard 同時跑時不會打架 |
| P0 | compose.py 支援 `--watch` 模式（spec 改變自動重 compose） | DX 大幅提升 |
| P1 | 補 `references/widget_<name>.md` 中的「invoke trigger」段落 | 讓 Claude 更容易選對 widget |
| P1 | 加 `widget table` 的 `data_compute` 支援（目前只支援 `data_source` path） | 跨 org 表格不用 hack |
| P1 | runtime 加 schema validation（spec 錯誤時給友善訊息） | 減少 silent fail |
| P2 | 加 `dark_mode` theme variant | 工程頁 / 後台場景 |
| P2 | 加 `line_chart` widget（等 RD 補 history API） | 解鎖趨勢類故事 |
| P2 | 加 `gauge` / `heatmap` widget | 新視覺類型 |
| P3 | 把 compose.py 包成 Python module，可在其他 Python 程式 import | 程式化集成 |

## Cross-skill dependencies

dashboard-builder 不直接呼叫 API，但讀取的 JSON 由這些 skill 產生：

| 用到的 JSON file（範例） | 產生它的 RD skill / op |
|---|---|
| `live-data/orgs.json` | `init-orgs.get_user_orgs` |
| `live-data/hierarchy.json` | `hvs.get_hierarchy_views` |
| `live-data/inventory.json` | `org-devices.get_inventory` |
| `live-data/licenses.json` | `org-licenses.get_licenses` |
| `live-data/memberships.json` | `team-members.get_org_memberships_overall` |
| `live-data/topology.json` | 多 op aggregate（`prototype/scripts/build_topology.sh` 是參考實作） |

⚠ **跨 org 聚合（如 topology.json）目前由 PMM 寫的 bash script 做**。長期建議 RD 包成一個 helper skill，例如 `multi-org-aggregator`，讓 Claude 直接呼叫而非依賴 shell script。

## 已知 limitation（不是 bug，是資料層）

詳見 [architecture-demo.html#limits](../architecture-demo.html#limits)：

- ❌ 沒有歷史聚合 API → 不能畫趨勢線
- ❌ 沒有 streaming（subscribe_*）script → 不能即時跳動
- ❌ 沒有實體拓樸 / cable 資料 → topology_tree 只能畫邏輯階層
- 🟡 沒有跨 org 成員聚合 → 需要 client-side 拼接

這些 limit 落在 RD 資料層，不是 dashboard-builder 的問題。但**請 RD 對齊 roadmap**——這些 API 補上後，line_chart / live_meter / map 等 widget 才有意義。

## 測試 checklist

整合完成後請 RD 跑：

```bash
# 1. 全部 5 個 spec 都能成功 compose
for spec in skills/dashboard-builder/examples/*.spec.json; do
  python skills/dashboard-builder/scripts/compose.py --spec "$spec" --out /tmp/test-$(basename "$spec" .spec.json).html
done

# 2. 視覺 QA（瀏覽器手動）
# - 每張 dashboard 載入 < 1 秒
# - 5 秒 auto-poll work
# - 跨 widget 點擊互動 work
# - Theme tokens 改一處能 cascade

# 3. 失敗情境
# - Missing live-data file → 該 widget 不會 crash，顯示 "—" 或 empty state
# - Spec 中 widget 名拼錯 → compose 階段 ValueError + 訊息清楚
# - Cycle in cross-widget events → 不會無限迴圈
```

## 聯絡窗口

- Spec / 文件問題 → Lulu Yeh (terrel.yeh@gmail.com)
- 視覺改進 → 直接編輯 `theme/` + `widgets/` PR-style
- 新增 widget → 參考 `references/index.md` 的 "Adding a new widget — checklist"
