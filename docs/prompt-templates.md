# Prompt Templates — Dashboard Builder

> **目的**：把 [`widget-catalog.md`](./widget-catalog.md) 的 11 個 widget schema 翻成「可以直接丟給 Claude 的 LLM 提示」。
>
> 給 Prompt Engineer / 後端 RD 抓來貼進 production 程式碼用。每個區塊都標明放哪個檔案、何時用。
>
> Last updated: YYYY-MM-DD · Owner: ___

---

## 整體架構（兩段式 LLM）

```
User input
    │
    ▼
┌───────────────────────────────┐
│  Stage 1 · Intent Parser      │  → Haiku (快、便宜)
│  prompts/parse_intent.md      │  Output: structured intent JSON
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│  Stage 2 · Widget Composer    │  → Sonnet (準確度高)
│  prompts/select_widgets.md    │  + Anthropic tool use API
│  + 11 個 tool definitions     │  Output: tool_use blocks
└───────────────┬───────────────┘
                │
                ▼
        Validated widget array
        (Zod schema 二次驗證)
                │
                ▼
        前端渲染
```

兩段拆開的好處：
- Stage 1 用 Haiku 解析意圖 → 便宜 (~10x 成本差)
- Stage 2 用 Sonnet 做組合 → 準確
- Stage 1 的輸出可以 cache（同 intent 不重複叫 Stage 2）

---

## Stage 1 · Intent Parser

**檔案**：`prompts/parse_intent.md`
**模型**：Claude Haiku 4.5
**輸入**：使用者自然語言
**輸出**：結構化 intent JSON

### System prompt

```markdown
You are a dashboard intent parser for an EnGenius network management product.

# Task
Parse the user's natural language request into structured intent JSON.
Output JSON only — no prose, no markdown, no explanation.

# Output schema (strict)
{
  "scope": "single_site" | "multi_site" | "single_device" | "topology",
  "time_range": "now" | "last_24h" | "last_7d" | "last_30d" | "last_90d",
  "metrics": ["client_count" | "anomaly_count" | "ap_load" | "poe_budget"
              | "channel_util" | "alerts" | "device_health" | "traffic_flow"],
  "audience": "smb_it" | "employee" | "pro",
  "intent_type": "snapshot" | "trend" | "ranking" | "drill_down" | "what_if",
  "refine_of": null | "<dashboard_id>"
}

# Rules
- 模糊需求預設 audience = "smb_it"
- 沒講時間範圍 → "last_7d"（除非問「現在」或「目前」→ "now"）
- 「再加一個 X」之類的 refine 句 → refine_of 帶上 dashboard_id
- 若使用者問「拓樸 / 影響範圍 / blast radius」→ scope = "topology"

# Few-shot examples

Input: 「我想看本週網路有沒有異常」
Output: {"scope":"single_site","time_range":"last_7d","metrics":["anomaly_count","client_count"],"audience":"smb_it","intent_type":"snapshot","refine_of":null}

Input: 「哪些 AP 太忙」
Output: {"scope":"single_site","time_range":"now","metrics":["ap_load"],"audience":"smb_it","intent_type":"ranking","refine_of":null}

Input: 「PoE 還剩多少」
Output: {"scope":"single_site","time_range":"now","metrics":["poe_budget"],"audience":"smb_it","intent_type":"snapshot","refine_of":null}

Input: 「AP-3F 壞掉會影響誰」
Output: {"scope":"topology","time_range":"now","metrics":["device_health"],"audience":"smb_it","intent_type":"drill_down","refine_of":null}

Input: 「訪客 Wi-Fi 流量都去哪了」
Output: {"scope":"single_site","time_range":"last_7d","metrics":["traffic_flow"],"audience":"smb_it","intent_type":"snapshot","refine_of":null}

Input: 「show top 5 sites by churn」
Output: {"scope":"multi_site","time_range":"last_30d","metrics":["device_health"],"audience":"smb_it","intent_type":"ranking","refine_of":null}

# User input
{{ user_prompt }}

# Output JSON only:
```

---

## Stage 2 · Widget Composer

**檔案**：`prompts/select_widgets.md` + 11 個 tool definitions
**模型**：Claude Sonnet 4.6
**輸入**：Stage 1 的 intent JSON
**輸出**：1-6 個 widget tool_use blocks

### Closed-set 約束的兩道防線

1. **Prompt 層**：system prompt 明確說「只能用以下 11 個 tool，不可發明」
2. **API 層**：用 Anthropic tool use 的 `tool_choice: { type: "any" }` — 模型「必須」呼叫某個 tool，不能輸出 free text。配合 `tools` 陣列只放這 11 個 → 物理上不可能輸出未定義的 widget。

第二道防線是真正的 closed-set 保證。Prompt 層只是輔助說明。

### System prompt

```markdown
You are a dashboard composer for EnGenius Network AI-Assistant.

# Task
Given a user intent (parsed JSON), select 1-6 widgets from the library to fulfill it.
You MUST call widget tools — do not output free text.

# Widget library (11 個，closed set，不可發明)

P0 (always available):
- render_kpi_card    → 單一數字 + 趨勢。適合：count / rate / score
- render_time_series → 折線 / 面積圖。適合：metric 隨時間變化
- render_bar_chart   → Top N 排名。適合：誰最忙 / 誰錯最多
- render_table       → 結構化清單。適合：多欄位資料 / 列表

P1 (general):
- render_status_grid → 大量設備健康燈號。適合：> 20 個 device 一覽
- render_heatmap     → 二維熱力圖。適合：時段 × 對象 (channel utilization 等)
- render_alert_list  → 告警清單。適合：嚴重程度排序的事件流
- render_gauge       → 弧形儀表。適合：utilization / capacity / 有上限的指標

P2 (advanced, networking-specific):
- render_site_map    → 地圖標點。適合：multi_site 的地理分布
- render_topology    → 網路拓樸圖。適合：blast radius / 上下游影響
- render_sankey      → 流量流向。適合：應用流量 / VLAN 流向

# Selection rules

1. **每個 metric 對應 1 個主 widget**，多 metric → 多 widget。
2. **intent_type 決定主視覺**：
   - snapshot → KPI Card / Gauge / Status Grid
   - trend → Time Series
   - ranking → Bar Chart / Table
   - drill_down → Table / Topology / Alert List
3. **scope 決定空間 widget**：
   - multi_site → Site Map
   - topology → Topology Graph
4. **audience = "employee"** → 限 1-2 個簡單 widget（KPI / Time Series 為主）。
5. **總 widget 數 ≤ 6**（PoC 限 4）。超過會讓使用者 overwhelm。
6. **refine_of != null** → 只回新增的 widget，不要重發既有 widget。
7. **何時用 Gauge 而不是 KPI Card**：metric 有合理上限（PoE budget、頻寬利用率、CPU）→ Gauge；無上限（客戶總數、anomaly 數）→ KPI Card。
8. **何時用 Topology 而不是 Site Map**：使用者問「影響誰 / 上下游 / blast radius」→ Topology；問「分點分布 / 哪個地區出事」→ Site Map。

# Output
Call widget tools directly. Each tool call is one widget on the dashboard.

# Intent
{{ intent_json }}
```

### API call shape (Anthropic SDK · TypeScript)

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { widgetTools } from "./widget-tools"; // 11 個 tool defs，下方產生方式

const client = new Anthropic();

const response = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 2048,
  system: SELECT_WIDGETS_SYSTEM_PROMPT,
  tools: widgetTools, // 11 個
  tool_choice: { type: "any" }, // 強制呼叫某個 tool
  messages: [
    { role: "user", content: JSON.stringify(intent) }
  ],
});

// 收齊所有 tool_use blocks → 即為 widget 陣列
const widgets = response.content
  .filter((b) => b.type === "tool_use")
  .map((b) => ({ type: b.name, spec: b.input }));
```

> ⚠️ **prompt caching**：`system` + `tools` 永遠不變 → 全部加 `cache_control` breakpoint，每次省 ~90% input tokens。見 [Anthropic prompt caching docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)。

---

## 11 個 Tool Definitions

從 Zod schema 自動產生，避免手寫兩份 drift。

### 從 Zod 產生 tool defs（推薦）

```typescript
// src/widgets/llm-tools.ts
import { zodToJsonSchema } from "zod-to-json-schema";
import { widgetRegistry } from "./registry";

export const widgetTools = Object.entries(widgetRegistry).map(([name, def]) => ({
  name: `render_${name}`,
  description: def.llmDescription, // 給 LLM 看的「何時用」
  input_schema: zodToJsonSchema(def.schema, { target: "openApi3" }),
}));
```

### 手寫範例（給沒用 Zod 的後端參考）

完整 11 個 tool 的 JSON Schema 太長 — 這裡列 3 個代表性的（其他依 [`widget-catalog.md`](./widget-catalog.md) 的 schema 翻譯即可）：

#### `render_kpi_card` (P0)

```json
{
  "name": "render_kpi_card",
  "description": "Render a KPI card showing a single metric value with optional trend arrow. Use when user wants the current value of one metric (e.g., '客戶數', 'anomaly 總數', '健康分數'). Do NOT use for metrics with a hard ceiling (use render_gauge instead).",
  "input_schema": {
    "type": "object",
    "properties": {
      "title": { "type": "string", "description": "短中文標題, e.g., '客戶數 (本週 vs 上週)'" },
      "value": { "type": ["number", "string"] },
      "delta": {
        "type": "object",
        "properties": {
          "value": { "type": "number" },
          "unit": { "type": "string", "enum": ["percent", "absolute"] },
          "direction": { "type": "string", "enum": ["up", "down"] }
        }
      },
      "comparison_label": { "type": "string", "description": "e.g., 'vs 上週'" },
      "trend": { "type": "string", "enum": ["good", "bad", "neutral"] }
    },
    "required": ["title", "value", "trend"]
  }
}
```

#### `render_gauge` (P1)

```json
{
  "name": "render_gauge",
  "description": "Render an arc gauge showing utilization or capacity. Use when the metric has a clear maximum (PoE budget, bandwidth %, CPU %, AP client cap). Visually communicates 'how close to ceiling'. Do NOT use for unbounded metrics like total client count.",
  "input_schema": {
    "type": "object",
    "properties": {
      "title": { "type": "string" },
      "value": { "type": "number", "description": "current value" },
      "max": { "type": "number", "description": "ceiling value (100% point)" },
      "unit": { "type": "string", "description": "e.g., '%', 'Mbps', 'W'" },
      "thresholds": {
        "type": "object",
        "properties": {
          "warning": { "type": "number", "description": "% of max for amber, e.g., 70" },
          "critical": { "type": "number", "description": "% of max for red, e.g., 90" }
        }
      },
      "format": { "type": "string", "enum": ["number", "percent", "bytes"] }
    },
    "required": ["title", "value", "max", "unit"]
  }
}
```

#### `render_topology` (P2)

```json
{
  "name": "render_topology",
  "description": "Render a network topology graph (nodes = devices, edges = links). Use for blast radius / upstream impact / 'who is affected when X breaks'. NOT for geographic site distribution (use render_site_map for that).",
  "input_schema": {
    "type": "object",
    "properties": {
      "title": { "type": "string" },
      "nodes": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "id": { "type": "string" },
            "label": { "type": "string" },
            "type": { "type": "string", "enum": ["router", "switch", "ap", "client", "gateway"] },
            "status": { "type": "string", "enum": ["good", "warning", "critical", "offline"] },
            "metric": { "type": "number" }
          },
          "required": ["id", "label", "type", "status"]
        }
      },
      "edges": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "from": { "type": "string" },
            "to": { "type": "string" },
            "health": { "type": "string", "enum": ["good", "degraded", "down"] },
            "label": { "type": "string" }
          },
          "required": ["from", "to", "health"]
        }
      },
      "layout": { "type": "string", "enum": ["force", "hierarchical", "manual"] }
    },
    "required": ["title", "nodes", "edges"]
  }
}
```

> 其他 8 個 tool 比照 [`widget-catalog.md`](./widget-catalog.md) 的 schema 一一翻譯。**不要手寫** — 用 `zodToJsonSchema()` 自動產生，schema 改動會自動同步。

---

## Few-shot Examples（對應 demo 的 8 個 scenario）

把這些塞進 Stage 2 system prompt 的 `# Examples` 區，能顯著提升選擇正確率。

| # | User intent | 預期 tool calls |
|---|---|---|
| 1 | 「我想看本週網路狀況」 | `render_kpi_card` × 3（客戶數 / anomaly / 健康分數）+ `render_time_series` × 1（anomaly 趨勢） |
| 2 | 「哪些 AP 太忙」 | `render_bar_chart` × 1 (top 10 by client count) |
| 3 | 「我的會議室 Wi-Fi 怎樣」 | `render_kpi_card` × 1（current 訊號）+ `render_time_series` × 1（最近 1h） |
| 4 | 「列出所有分點健康狀況」 | `render_site_map` × 1 + `render_table` × 1（明細） |
| 5 | 「AP-3F-N2 最近連線怎樣」 | `render_time_series` × 1（client 數）+ `render_alert_list` × 1（最近事件） |
| 6 | 「訪客 Wi-Fi 用了多少」 | `render_sankey` × 1（流向）+ `render_kpi_card` × 1（總流量） |
| 7 | 「PoE 還夠不夠插新設備」 | `render_gauge` × 1（PoE budget）+ `render_table` × 1（current 用量分布） |
| 8 | 「這台 switch 壞了會影響誰」 | `render_topology` × 1（hierarchical layout）+ `render_alert_list` × 1 |

### 範例：scenario 7 完整 few-shot

```markdown
# Example: PoE capacity check

User intent:
{"scope":"single_site","time_range":"now","metrics":["poe_budget"],"audience":"smb_it","intent_type":"snapshot","refine_of":null}

Expected tool calls:
1. render_gauge({
    "title": "PoE budget · SW-1F",
    "value": 287, "max": 370, "unit": "W",
    "thresholds": {"warning": 70, "critical": 90},
    "format": "number"
  })
2. render_table({
    "title": "PoE 用量分布",
    "columns": [
      {"key":"port","label":"Port","type":"text"},
      {"key":"device","label":"設備","type":"text"},
      {"key":"watt","label":"瓦數","type":"number"}
    ],
    "rows": [...]
  })
```

---

## Validation 與 Fallback

LLM 偶爾會產出不合 schema 的 tool input — 後端要二次驗證。

```typescript
import { z } from "zod";
import { widgetRegistry } from "./registry";

function validateWidget(toolName: string, input: unknown) {
  const widgetType = toolName.replace(/^render_/, "");
  const schema = widgetRegistry[widgetType]?.schema;
  if (!schema) {
    return { ok: false, error: "unknown_widget_type" };
  }
  const result = schema.safeParse(input);
  if (!result.success) {
    // Fallback: KPI card with error message
    return {
      ok: false,
      error: result.error.issues,
      fallback: { type: "kpi", title: "Widget 載入失敗", value: "—", trend: "neutral" }
    };
  }
  return { ok: true, widget: result.data };
}
```

---

## Eval Cases（最低 30 個）

Production 上線前，每個 widget 至少 5 個 golden case：

| Widget | 必測 case |
|---|---|
| KPI Card | 正常數字 / 0 / 負數 / null delta / 中文 title |
| Time Series | 1 條線 / 多條線 / 空資料 / 跨夜時間軸 / category 軸 |
| Bar Chart | 5 項 / 1 項 / horizontal / 全部相同值 / 含 highlight |
| Table | 全欄位 / 缺欄位 / 含 badge / 排序 / max_rows 截斷 |
| Status Grid | 全 good / 全 critical / 混合 / > 100 設備 / score=0 |
| Heatmap | 24h × 7d / 空 cell / 全 0 / 極端值 / diverging scale |
| Alert List | 全 critical / 全 info / 空清單 / > 50 筆 / 同設備多 alert |
| Gauge | < warning / warning / critical / value > max（保護） / unit 變化 |
| Site Map | 1 site / 100 sites / 無 lat/lon → fallback / 跨洲 |
| Topology | 線性 chain / 樹狀 / 有環 / disconnected node / > 50 nodes |
| Sankey | 1 → 1 / 1 → N / 多層 / value=0 / 同 source 多 target |

跑 eval 的 D1/D2/D3 標準見 [`dashboard-builder-implementation.html` Tab 3](../dashboard-builder-implementation.html#t3)。

---

## 維護紀律

- **Schema 改動**：先改 [`widget-catalog.md`](./widget-catalog.md) → 改 Zod → 自動 regenerate tool defs → 新增 eval case
- **新增第 12 個 widget**：走 RFC 流程（見 implementation.html Tab 4「未來擴充」），不要 sprint task 直接加
- **Few-shot 更新**：每加一個 widget 至少配 1 個 few-shot；每 quarter review 一次正確率回頭調整

---

## 相關文件

- [widget-catalog.md](./widget-catalog.md) — 11 widget input schema 詳細規格（這份文件的 source）
- [dashboard-builder-implementation-guide.md](./dashboard-builder-implementation-guide.md) — Pre-kickoff 工程準備
- [../dashboard-builder-implementation.html](../dashboard-builder-implementation.html) — 工程實作指南（4-tab 互動頁，含 eval pipeline）
