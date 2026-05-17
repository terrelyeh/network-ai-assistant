# History Aggregation API · 提案文件 · 🔶 PLAN B Fallback

> ⚠ **這份文件的定位 reframed（2026-05-17）**：
>
> 原本以為「RD 還沒做歷史 API，所以要從零提議建一套」。但**仔細想想 EnGenius Cloud GUI 已經有顯示 throughput / client count / HVS 趨勢 chart**，代表 backend **必然已經持久化歷史數據 + 已經有 GUI 在 call 的 endpoint**。
>
> 所以 **Plan A** 是 [`06-api-doc-questions.md` Q9](06-api-doc-questions.md#q9-history-data-api--應該是-documentation-gap不是-architecture-gap) — 5 分鐘的 ask：「請告訴我 GUI 用哪個 endpoint 拿歷史數據？」
>
> **這份 04 是 Plan B** — 萬一真的問下去發現 GUI 是用內部微服務拼出來的、沒有對外乾淨的 history API，才會走這條 3 工作週的 backend 投資路線。

---

> 給：下次 RD meeting · Plan B 情境用
> Priority（fallback）: P2 — 只在 Plan A 失敗時觸發
> 預估 backend: 2-3 工作週

## TL;DR · Plan B 情境

如果 RD 確認 **沒有對外可用的 history API** 給我們包成 skill，那就需要走這份提案的方向 — 從零建一條 time-series persistence + aggregation 的 pipeline。

提議：新增一個 history aggregation endpoint，讓 dashboard-builder 解鎖 line_chart / sparkline / area_chart 三個 widget。

> **但請先確認**：Plan A（GUI 用的 endpoint 分享出來）是不是 5 分鐘就能解決的事？大部分情況答案是 yes，這份 Plan B 就用不到。

---

## 為什麼這個阻擋一整個品類

| 現有 dashboard 類型 | 能不能做 | 例 |
|---|---|---|
| 當前狀態 view（org health、device list） | ✅ 已 5 張 | org-health / off-boarding / license-renewal / multi-org-gov / cross-org-realloc |
| 構成分布 view（% breakdown） | ✅ 已 1 張 | multi-org-governance 用 donut |
| 矩陣交叉 view | ✅ 已 1 張 | cross-org-reallocation 用 heatmap |
| **趨勢類 view** | ❌ 完全不行 | 過去 N 天 throughput / client growth / license burn |
| **預測類 view** | ❌ 完全不行（趨勢的延伸）| 「再 3 個月會用完所有 license」 |

→ **客戶最常問的「給我看趨勢」我們無法回應**。這是 enterprise IT manager 的基本訴求。

---

## 提議 API endpoint

### 主要 endpoint

```
GET /v2/orgs/{orgId}/metrics/aggregate
```

### Query params

| name | type | required | description |
|---|---|---|---|
| `metric` | string | yes | one of: `throughput` / `client_count` / `cpu_load` / `memory_usage` / `link_status` / `wan_latency` |
| `from` | ISO8601 | yes | 起始時間 |
| `to` | ISO8601 | yes | 結束時間 |
| `groupBy` | string | yes | `minute` / `hour` / `day` / `week` |
| `targetType` | string | yes | `device` / `network` / `org` |
| `targetId` | string | yes | 對應 targetType 的 ID（device_mac / network_id / org_id）|
| `aggregation` | string | no | `avg`（default）/ `sum` / `max` / `min` / `p95` / `p99` |
| `band` | string | no | 只對 wifi metric 適用：`2.4` / `5` / `6` |

### Response

```jsonc
{
  "metric": "throughput",
  "unit": "B/s",
  "groupBy": "hour",
  "from": "2026-05-10T00:00:00Z",
  "to":   "2026-05-16T00:00:00Z",
  "aggregation": "avg",
  "targetType": "network",
  "targetId": "5ea283a1d5f6b23a755a7d57",

  "points": [
    { "timestamp": 1715299200000, "value": 12450000 },
    { "timestamp": 1715302800000, "value": 18760000 },
    { "timestamp": 1715306400000, "value":  9230000 },
    // ... one per groupBy bucket
  ],

  "summary": {
    "min": 5000000,
    "max": 25000000,
    "mean": 14200000,
    "p95": 22500000,
    "trend": "stable | increasing | decreasing"   // optional helper
  }
}
```

### Error cases

| HTTP | When |
|---|---|
| 400 | invalid combination (e.g. groupBy=minute, range > 24h) |
| 403 | RBAC: caller doesn't have read access to target |
| 416 | range out of retention (e.g. >90 days ago) |
| 503 | history pipeline temporarily down |

---

## MVP vs Full Scope（分階段做）

### MVP（First 2 weeks）

最少做 3 個 metric：

| metric | 解鎖什麼 dashboard |
|---|---|
| `throughput` | network 流量趨勢、找出高峰時段 |
| `client_count` | client 數變化、容量規劃 |
| `cpu_load` | 設備健康度長期趨勢 |

支援 `groupBy: hour / day / week`，retention >= 30 days。

### Phase 2（追加 metric）

| metric | 解鎖 |
|---|---|
| `memory_usage` | 進階 health monitor |
| `link_status` | port 穩定性 |
| `wan_latency` | gateway 健康 |

### Phase 3（進階聚合）

- `groupBy: minute`（高解析度，retention shorter，e.g. 24h）
- Cross-device aggregation（all APs in network）

---

## 對應 dashboard widget 解鎖

補完 history API 後，dashboard-builder 可加 3 個 widget：

### Widget A. `line_chart`

```jsonc
{
  "widget": "line_chart",
  "title": "Past 7 Days Throughput",
  "data_source": {
    "type": "history_aggregate",
    "metric": "throughput",
    "targetType": "network",
    "targetId_path": "active_network_id",
    "groupBy": "hour",
    "duration": "P7D"
  },
  "x_axis": "timestamp",
  "y_axis": "value",
  "y_unit": "MB/s",
  "annotations": [
    { "type": "max_marker" },
    { "type": "trend_line" }
  ]
}
```

### Widget B. `sparkline`

```jsonc
{
  "widget": "table",
  "columns": [
    { "label": "Device", "field": "name" },
    {
      "label": "7d throughput",
      "render": "sparkline",      ← NEW renderer
      "data_source": {
        "type": "history_aggregate",
        "metric": "throughput",
        "targetType": "device",
        "targetId_field": "mac",
        "groupBy": "hour",
        "duration": "P7D"
      }
    }
  ]
}
```

### Widget C. `area_chart`

累積量 / stacked。例如 stacked client_count by band。

---

## 工作量估計（給 RD 參考）

| 階段 | 工作項 | 估時 |
|---|---|---|
| **Schema design** | 跟 PMM 對齊 metric 名 + unit 標準 | 2 天 |
| **Backend pipeline** | metric → time-series store（如 InfluxDB / Timescale）的 ingestion | 1 工作週 |
| **Aggregation layer** | 把現有 collection 接到 time-series store + 補 backfill 至少 30 天 | 1 工作週 |
| **API endpoint** | 包成上面 spec | 3-5 天 |
| **QA + retention testing** | | 3 天 |
| **PMM widget side** | line_chart / sparkline / area_chart widget + ref docs | 1 工作週（並行）|

**最樂觀**：3 週後 MVP 上線、widget 跟著 ready。

---

## 開放問題（會議要討論）

1. **time-series store 用什麼？** Influx / Timescale / 自建？
2. **retention 多久？** 30 / 90 / 180 / 360 天？影響 storage 成本。
3. **要不要支援 multi-device aggregation？**（all APs in network 的 sum/avg）
4. **誰有權限呼叫？** RBAC scoping 怎麼定？
5. **跟現有 collection 框架的整合**：collection 已經在跑了嗎？還是要從零做？
6. **GUI 是否同步用這個 endpoint？** 還是 dashboard-builder 獨佔？

---

## 建議下次會議 agenda（30 min）

- 0-5 min: 為什麼需要 history（demo 故事 + 競爭比較）
- 5-15 min: 過上面提議 spec
- 15-25 min: 討論 6 個開放問題
- 25-30 min: 對齊 MVP scope + owner + tentative timeline

---

## 如果 RD 說「先做 MVP 就好」我們怎麼回應

✅ **完全 OK**。我們也建議 MVP-first。

| 階段 | 不可少 | 可砍 |
|---|---|---|
| MVP | throughput / client_count / cpu_load 3 個 metric，groupBy=hour/day，retention >= 30 days | minute 解析度、跨 device 聚合、trend hint |
| Phase 2 | 補其餘 metric | 進階聚合 |
| Phase 3 | 進階查詢 | 預測 |

只要 MVP 那 3 個 metric 上線，dashboard-builder 立刻能做出至少 2 個新 dashboard 類型。

---

## 如果 RD 說「3 個月做不出來」我們怎麼回應

🟡 退讓選項：

- 只做 `throughput` 1 個 metric MVP（4-5 工作週）
- Retention 縮到 7 天（demo 用、production 之後擴）
- 用既有 monitoring service (e.g. Prometheus) 直接接前端，跳過自建 pipeline

最差也要拿到「throughput, 7-day retention, hourly granularity」這條最小路徑，否則整個 sprint 報廢。
