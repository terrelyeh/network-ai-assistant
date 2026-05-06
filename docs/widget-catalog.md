# Widget Catalog — Dashboard Builder

> **目的**：定義 LLM 可以組合的 widget 集合 + 每個 widget 的 input/output 契約。
> 這份文件是 **LLM prompt eng**、**前端 RD**、**Design** 三方對齊的單一來源。
> 
> Last updated: YYYY-MM-DD · Owner: ___

---

## 為什麼需要這份文件

- **LLM**：只能從這份 catalog 選 widget（closed set），不能發明新類型
- **前端 RD**：只要實作這 N 個 widget component，輸入 schema 永遠不變
- **Design**：每個 widget 只畫一次視覺，所有 dashboard 都符合 EnGenius 視覺語言
- **Demo / 業務**：「我們能做什麼」邊界清楚，不會被客戶問倒

---

## Widget 列表（v1 限定 8 種）

| # | Widget | Tool name | 主要用途 | 優先級 |
|---|---|---|---|---|
| 1 | KPI Card | `render_kpi_card` | 單一數字 + 趨勢 | P0 ✅ MVP |
| 2 | Time Series | `render_time_series` | 趨勢線 / 面積圖 | P0 ✅ MVP |
| 3 | Bar Chart | `render_bar_chart` | Top N / 排名 | P0 ✅ MVP |
| 4 | Table | `render_table` | 結構化清單 | P0 ✅ MVP |
| 5 | Status Grid | `render_status_grid` | 設備健康燈號 | P1 |
| 6 | Heatmap | `render_heatmap` | 時間 × 維度熱力 | P1 |
| 7 | Alert List | `render_alert_list` | 告警清單 | P1 |
| 8 | Site Map | `render_site_map` | 地理 / 拓樸分布 | P2 |

> P0 是 MVP 必要 — 跑通整個 loop 用這 4 種就夠（驗證 wedge thesis 不需要 8 個都做）。
> P1/P2 等 P0 通了再補。

---

## Widget 詳細 Spec

### 1. KPI Card

**Tool name**: `render_kpi_card`

**用途**：顯示單一指標（一個數字 + 變化方向 + 比較期間）。Dashboard 最常見的「summary 區塊」。

**Input schema**:
```json
{
  "title": "string",          // e.g., "客戶數 (本週 vs 上週)"
  "value": "number | string", // e.g., 847 or "12.4 GB"
  "delta": {                  // optional
    "value": "number",        // e.g., 12.4
    "unit": "percent | absolute",
    "direction": "up | down"
  },
  "comparison_label": "string", // e.g., "vs 上週", "vs 7 天平均"
  "trend": "good | bad | neutral" // 顏色 hint，前端決定怎麼染色
}
```

**範例 JSON**:
```json
{
  "title": "本週 anomaly 總數",
  "value": 23,
  "delta": { "value": 8, "unit": "percent", "direction": "down" },
  "comparison_label": "vs 上週",
  "trend": "good"
}
```

**視覺 spec**：
- 參考既有 EnGenius dashboard 的「Stat block」樣式
- 大數字 48-64px，title 12-13px UPPERCASE muted
- delta 用 ↑↓ 箭頭 + 顏色（green=good, red=bad）
- 卡片 padding 24-28px，border-radius 12px

**Reference image**: `docs/widget-refs/kpi-card.png` （TODO）

**LLM 使用時機**：
- 使用者問「整體狀況怎樣」、「比上週好還差」、「現在數量多少」
- Dashboard 上方做 summary row（通常 3-5 個 KPI 並排）

---

### 2. Time Series

**Tool name**: `render_time_series`

**用途**：時間軸趨勢線 / 面積圖 / 多條線比較。看「隨時間變化」的問題。

**Input schema**:
```json
{
  "title": "string",
  "x_axis": {
    "label": "string",           // e.g., "週一-週日", "Last 7 days"
    "type": "datetime | category"
  },
  "y_axis": {
    "label": "string",           // e.g., "Anomaly 數量"
    "unit": "string"             // e.g., "count", "%", "Mbps"
  },
  "series": [
    {
      "name": "string",          // e.g., "本週", "上週"
      "data": [                  // array of points
        { "x": "2026-05-01", "y": 12 },
        { "x": "2026-05-02", "y": 15 }
      ],
      "style": "line | area | dashed"
    }
  ]
}
```

**範例 JSON**:
```json
{
  "title": "本週 Anomaly 趨勢",
  "x_axis": { "label": "Day of week", "type": "category" },
  "y_axis": { "label": "Count", "unit": "count" },
  "series": [
    { "name": "本週", "style": "area",
      "data": [{"x":"週一","y":3},{"x":"週二","y":2},{"x":"週三","y":4},{"x":"週四","y":5},{"x":"週五","y":3},{"x":"週六","y":4},{"x":"週日","y":2}] }
  ]
}
```

**視覺 spec**：
- 主色用 EnGenius accent（`#03A9F4` cyan 或產品橘 `#ff6b35` 看 context）
- 多條線時用 categorical palette（不超過 5 條）
- area 模式漸層淡入到 transparent
- grid line 淺灰、不搶眼

**Reference image**: `docs/widget-refs/time-series.png` （TODO）

**LLM 使用時機**：
- 使用者問「過去 N 天/週/月 怎麼變」
- 看週期性、突波、趨勢

---

### 3. Bar Chart

**Tool name**: `render_bar_chart`

**用途**：Top N 排名、類別比較、橫條 / 直條皆可。

**Input schema**:
```json
{
  "title": "string",
  "orientation": "horizontal | vertical",
  "data": [
    {
      "label": "string",      // e.g., "AP-7F-N3"
      "value": "number",
      "highlight": "boolean"  // optional, 標紅讓使用者注意
    }
  ],
  "value_label": "string",    // e.g., "Sticky clients", "Errors"
  "max_items": "number"       // 限制顯示前 N 個（推薦 5-10）
}
```

**範例 JSON**:
```json
{
  "title": "Top 5 問題設備",
  "orientation": "horizontal",
  "value_label": "錯誤次數",
  "data": [
    { "label": "AP-7F-N3", "value": 47, "highlight": true },
    { "label": "SW-1F-Gi12", "value": 32 },
    { "label": "AP-3F-S2", "value": 28 }
  ]
}
```

**視覺 spec**：
- Highlight bar 用 red/orange，其他 cyan
- Bar 圓角，間距均勻
- value 標籤直接顯示在 bar 末端（不放右邊空欄）

**Reference image**: `docs/widget-refs/bar-chart.png` （TODO）

**LLM 使用時機**：
- 使用者問「前 N 名」、「誰最忙」、「誰錯最多」
- 跨 site / device / metric 排名

---

### 4. Table

**Tool name**: `render_table`

**用途**：結構化清單，多欄位資料。每列可帶 status badge。

**Input schema**:
```json
{
  "title": "string",
  "columns": [
    { "key": "string", "label": "string", "type": "text | number | badge | timestamp" }
  ],
  "rows": [
    {
      "cells": {
        "device": "AP-7F-N3",
        "issue": "Sticky clients",
        "status": { "label": "嚴重", "level": "critical" }
      }
    }
  ],
  "max_rows": "number"
}
```

**範例 JSON**:
```json
{
  "title": "Top 5 問題設備",
  "columns": [
    { "key": "device", "label": "設備", "type": "text" },
    { "key": "issue", "label": "類型", "type": "text" },
    { "key": "status", "label": "狀態", "type": "badge" }
  ],
  "rows": [
    { "cells": { "device": "AP-7F-N3", "issue": "Sticky clients", "status": { "label": "嚴重", "level": "critical" } } }
  ]
}
```

**視覺 spec**：
- Header row dim/uppercase
- Badge 配色：critical=red / warning=amber / ok=green / info=cyan
- Hover row 微亮，不放 expand 動作（這是 read-only widget）

**Reference image**: `docs/widget-refs/table.png` （TODO）

**LLM 使用時機**：
- 使用者問「列出 N 個 X」
- 多欄位細節需要一覽

---

### 5. Status Grid (P1)

**Tool name**: `render_status_grid`

**用途**：N 個 site / device 的健康燈號 mini grid，一眼看哪邊紅。

**Input schema**:
```json
{
  "title": "string",
  "items": [
    {
      "label": "string",       // e.g., "HQ", "Branch A"
      "score": "number",       // 0-100
      "status": "good | warning | critical",
      "sub": "string"          // optional, e.g., "94" 顯示在卡片中
    }
  ]
}
```

**Reference image**: `docs/widget-refs/status-grid.png` （TODO）

---

### 6. Heatmap (P1)

**Tool name**: `render_heatmap`

**用途**：時間 × 維度的熱力圖。e.g., 一週 × 24 小時的負載熱力。

**Input schema**:
```json
{
  "title": "string",
  "x_axis": { "label": "string", "categories": ["string"] },
  "y_axis": { "label": "string", "categories": ["string"] },
  "cells": [
    { "x": "string", "y": "string", "value": "number" }
  ],
  "color_scale": "sequential | diverging"
}
```

**Reference image**: `docs/widget-refs/heatmap.png` （TODO）

---

### 7. Alert List (P1)

**Tool name**: `render_alert_list`

**用途**：告警清單。每筆有 severity / 時間 / 設備 / 描述。

**Input schema**:
```json
{
  "title": "string",
  "alerts": [
    {
      "severity": "critical | warning | info",
      "timestamp": "ISO 8601",
      "device": "string",
      "message": "string",
      "action_label": "string"  // optional, e.g., "查看 →"
    }
  ]
}
```

**Reference image**: `docs/widget-refs/alert-list.png` （TODO）

---

### 8. Site Map (P2)

**Tool name**: `render_site_map`

**用途**：地圖或拓樸圖呈現 site 分布。最複雜，留 P2。

**Input schema**:
```json
{
  "title": "string",
  "mode": "geo | topology",
  "nodes": [
    { "id": "string", "label": "string", "lat": "number", "lon": "number", "status": "good | warning | critical" }
  ],
  "edges": [  // topology mode 才用
    { "from": "string", "to": "string" }
  ]
}
```

**Reference image**: `docs/widget-refs/site-map.png` （TODO）

---

## RD 實作 Checklist

每個 widget 要交付：

- [ ] React/Vue component（`<KpiCard {...spec} />` 之類）
- [ ] Input schema validation（Zod / TypeBox / JSON Schema）
- [ ] Storybook story（4-6 種 input 變化）
- [ ] Loading skeleton 樣式
- [ ] Error state（schema 不合法時的 fallback）
- [ ] Responsive（手機壞掉的話至少不要爆版）

---

## LLM Prompt Engineering Checklist

- [ ] System prompt 列出 catalog（這份文件 paste 進去）
- [ ] 每個 widget 一個 tool definition（schema 對齊上面）
- [ ] Few-shot examples：取 8 個 scenario 各 1 組（user query → tool calls）
- [ ] Closed-set rule：「只能用 catalog 裡的 widget，不能發明」
- [ ] Combo rules：dashboard 上限 widget 數量（建議 ≤ 6）

---

## Open Questions

- [ ] 資料來源：widget 的 data 從哪打？走 API gateway 統一收 / 還是 widget 各自打 SQL？
- [ ] Cache：相同 query 5 分鐘內重打要不要重 render？
- [ ] 客製化：使用者能不能改 widget 的 title / 顏色？（v1 建議不行）
- [ ] 儲存格式：dashboard 的 JSON spec 要存在哪 — DB? 使用者本地?
- [ ] 多語：widget label 要不要 i18n key 化？
