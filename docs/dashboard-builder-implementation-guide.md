# Dashboard Builder 前端實作準備指南

> **給誰看**：PM、RD lead、Design lead、Prompt Engineer
> **目的**：在動手 coding 之前，內部對齊「該怎麼準備、誰先做、做到什麼程度」
> **前置閱讀**：[widget-catalog.md](./widget-catalog.md)（widget 規格細節）
> Last updated: 2026-05-06

---

## TL;DR

1. **不要先寫 Design Guideline** — EnGenius Cloud 已有設計語言，重寫只會打架
2. **先做 Widget Catalog**（Source of truth：Zod schema），這是 LLM ↔ 前端 ↔ Design 三方對齊的契約
3. **Schema 先於 UI library** — schema 反映 LLM 自然吐什麼，不被 library 綁架
4. **第一版只做 P0 4 個 widget 跑通 end-to-end**（KPI / Time Series / Bar / Table），通了再擴

---

## 1. 為什麼不先寫 Design Guideline

### 結論
- 你們**已經有 EnGenius Cloud GUI** = 已經有 design system，只是沒寫成文件
- 重寫一份 Design Guideline = 至少 3 週，做完還會跟既有 GUI 不一致
- Wedge product 6-8 週要見驗證結果，等不了 design system 文件成型

### 替代做法（半天搞定）
從既有 EnGenius Cloud dashboard 直接抓 design tokens：
- 主色（accent color）
- 字體 / 字級階層
- Card padding / border-radius
- Chart 配色
- Spacing scale

整理成一份 `design-tokens.md` 或 Figma frame，**RD render widget 時直接 reuse 既有 css variables / tailwind tokens**，不會跟既有產品違和。

> ⚠️ 這份 design tokens **不是 design guideline** — 它是「對齊既有」的快照，不是另寫一套規則。

---

## 2. 什麼是 Widget Catalog

### 一句話
**LLM 跟前端之間的「元件菜單」+ 契約** — 預先定義 11 種 widget「樂高積木」（P0 4 + P1 4 + P2 3），AI 只能從中挑、再組合。

### 為什麼需要

| 沒有 catalog | 有 catalog |
|---|---|
| LLM 會 hallucinate 出前端做不出來的 chart | LLM 只能挑 11 個已知 widget |
| 前端要處理 unexpected schema | 前端只實作 11 個 component，輸入永遠對齊 |
| Design 跟不上 AI 的天馬行空 | Design 只畫 11 種，AI 組出來都符合視覺語言 |
| Demo 給客戶時邊界模糊 | 「我們能做什麼」一目了然 |

### 工作流程示意

```
使用者：「我想看這週網路有沒有什麼異常」
                ↓
LLM 看 catalog → 決定組合：
                ├─ KPI Card × 3      (客戶數 / anomaly 總數 / 健康分數)
                ├─ Time Series × 1   (anomaly 趨勢)
                ├─ Table × 1         (Top 5 問題設備)
                └─ Site Map × 1      (各 site 健康分布)
                ↓
前端拿到 widget JSON → 渲染
```

### 業界對應名詞

「Widget Catalog」**不是嚴格的業界專有名詞**，但這個 *概念* 業界用得很普遍：

| 來源 | 同類叫法 |
|---|---|
| Anthropic / OpenAI | **Tool definitions** |
| Notion | Block types |
| Slack | **Block Kit** |
| Grafana | Panel types |
| Tableau / Looker | Visualizations |
| Streamlit | Components |
| shadcn / Radix | Component library |

**共通本質**：closed set of pre-defined building blocks + 每個 block 有明確 input schema。內部你愛叫什麼都行（`WidgetSpec` / `Component Library` / `Tool Registry`），重點是概念對齊。

---

## 3. Widget Catalog 的實際存在形式

業界做法：**三份東西，但只有「一份 source of truth」**。

### 架構圖

```
            ┌─────────────────────────────────┐
            │   Source of Truth               │
            │   widgets/schemas/*.ts (Zod)    │
            │   widgets/registry.ts           │
            └────────────┬────────────────────┘
                         │ 自動產出
            ┌────────────┴────────────┐
            ▼                         ▼
    ┌──────────────┐          ┌─────────────────┐
    │ LLM tool spec│          │  TypeScript     │
    │ (JSON array) │          │  Component Props│
    └──────────────┘          └─────────────────┘
            │                         │
            ▼                         ▼
        給 LLM API              給前端 components
```

### 每個層級的形式

| 層級 | 形式 | 檔案數 | 給誰 |
|---|---|---|---|
| **Source of truth** | TypeScript + Zod schemas | 一個 widget 一份 | RD（核心檔） |
| **LLM tool spec** | JSON array (auto-generated) | 一份合併 | LLM API |
| **Component library** | React/Vue components | 一個 widget 一份 | 前端渲染 |
| **Storybook stories** | `.stories.tsx` | 一個 widget 一份 | RD + Design |
| **人看版 Markdown** | `widget-catalog.md` | 一份合併 | PM / 業務 / 客戶 |

### 範例資料夾結構

```
src/widgets/
├── schemas/                  ← Source of truth（一份/widget）
│   ├── kpi-card.ts          ← Zod schema
│   ├── time-series.ts
│   ├── bar-chart.ts
│   └── table.ts
├── components/               ← 前端 component（一份/widget）
│   ├── KpiCard.tsx
│   ├── TimeSeries.tsx
│   ├── BarChart.tsx
│   └── Table.tsx
├── stories/                  ← Storybook
│   ├── KpiCard.stories.tsx
│   └── ...
├── registry.ts               ← 集中註冊（schema + component 對應）
└── llm-tools.ts              ← 自動產出 LLM tool spec

docs/
└── widget-catalog.md         ← 人看的版本
```

---

## 4. Zod 是什麼？為什麼用它

Zod 是 TypeScript 圈最紅的 schema validation 函式庫。**寫一次 schema，同時得到三個東西**：

1. TypeScript 型別（compile time）
2. Runtime validation（reject 壞資料）
3. JSON Schema（可轉成 LLM tool spec）

### 範例

```typescript
import { z } from 'zod';

// 1. 定義 schema
const KpiCard = z.object({
  title: z.string(),
  value: z.union([z.number(), z.string()]),
  delta: z.object({
    value: z.number(),
    direction: z.enum(['up', 'down']),
    unit: z.enum(['percent', 'absolute'])
  }).optional(),
  trend: z.enum(['good', 'bad', 'neutral'])
});

// 2. 自動拿到 TypeScript 型別
type KpiCardProps = z.infer<typeof KpiCard>;

// 3. Runtime 驗證（LLM 回傳 JSON 進來時用）
KpiCard.parse({ title: "本週客戶", value: 847, trend: "good" });  // ✓
KpiCard.parse({ title: "本週客戶", value: "x" });                  // ✗ throws

// 4. 轉成 JSON Schema（給 LLM）
import { zodToJsonSchema } from 'zod-to-json-schema';
const llmToolSchema = zodToJsonSchema(KpiCard);
```

### 其他生態系

| Stack | 對應方案 |
|---|---|
| Python | **Pydantic**（FastAPI 用的） |
| TypeScript（新） | **TypeBox**（直接產 JSON Schema） |
| TypeScript（舊） | io-ts、Yup |

### 為什麼 Zod 適合 Widget Catalog

- LLM 吐 JSON 進來 → Zod 驗證一次（壞掉直接 reject，不會炸前端）
- TypeScript component props 直接用 `z.infer<>` → schema 改了，component 自動有 type error
- 一份 schema 自動產出 LLM tool spec（不用手寫對齊兩份）

---

## 5. 怎麼開始做（順序很重要）

### ⚠️ 錯誤順序（很常見）

> 先挑 UI library → 看 component 有什麼 props → 倒回去寫 schema

這會讓 schema 被 library 綁架。例如挑了 Recharts，schema 會冒出 Recharts 特有的 prop（`activeIndex`、`legendType`），LLM 完全不知道要幹嘛。

### ✅ 正確順序

#### Step 1：先想 LLM 的「資訊輸入」

不看 UI，先問：「使用者問了 X，AI 需要吐什麼資料才足以畫這個 widget？」

```typescript
// KPI Card：使用者要看一個數字 + 變化
const KpiCard = z.object({
  title: z.string(),
  value: z.union([z.number(), z.string()]),
  delta: z.object({
    value: z.number(),
    direction: z.enum(['up', 'down']),
    unit: z.enum(['percent', 'absolute'])
  }).optional(),
  trend: z.enum(['good', 'bad', 'neutral'])
});
```

這份 schema **不依賴任何 UI library** — 換 React/Vue/Svelte 都不影響。

#### Step 2：再選 UI library 渲染

**優先看既有 EnGenius Cloud 用什麼，reuse 比新挑爽 library 重要**。

如果是 React stack：

| 用途 | 推薦 library |
|---|---|
| 圖表（Time Series / Bar / Heatmap） | **Recharts**（簡單）/ **Apache ECharts**（強大）/ **Tremor**（dashboard-styled） |
| KPI Card / Status Grid / Alert List | **shadcn/ui**（Tailwind） / 自己用 Tailwind 寫 |
| Table | **TanStack Table**（headless）/ shadcn Table |
| Site Map / 地圖 | **Mapbox GL** / **Leaflet** |

Vue stack 對應：**Naive UI** / **Element Plus** / **Vue-ECharts**。

#### Step 3：Component 接 Zod 型別

```typescript
import { KpiCardSchema } from './schemas/kpi-card';

type Props = z.infer<typeof KpiCardSchema>;

export function KpiCard({ title, value, delta, trend }: Props) {
  return (
    <div className="rounded-xl border p-6">
      <div className="text-xs uppercase text-muted">{title}</div>
      <div className="text-5xl font-bold">{value}</div>
      {delta && (
        <div className={trend === 'good' ? 'text-green-500' : 'text-red-500'}>
          {delta.direction === 'up' ? '↑' : '↓'} {delta.value}
          {delta.unit === 'percent' ? '%' : ''}
        </div>
      )}
    </div>
  );
}
```

#### Step 4：註冊到 registry

```typescript
// src/widgets/registry.ts
import { KpiCardSchema, KpiCard } from './kpi-card';
import { TimeSeriesSchema, TimeSeries } from './time-series';

export const WIDGET_REGISTRY = {
  render_kpi_card: {
    schema: KpiCardSchema,
    component: KpiCard,
    description: '顯示單一指標 + 趨勢方向',
  },
  render_time_series: {
    schema: TimeSeriesSchema,
    component: TimeSeries,
    description: '時間軸趨勢線 / 面積圖',
  },
  // ...
} as const;
```

#### Step 5：自動產出 LLM tool spec

```typescript
// src/widgets/llm-tools.ts
import { zodToJsonSchema } from 'zod-to-json-schema';
import { WIDGET_REGISTRY } from './registry';

export const LLM_TOOLS = Object.entries(WIDGET_REGISTRY).map(([name, def]) => ({
  name,
  description: def.description,
  input_schema: zodToJsonSchema(def.schema),
}));

// 直接餵給 Anthropic / OpenAI API
```

---

## 6. 角色分工 / 並行進度

```
週 1                週 2-3              週 4-6
─────────────────  ─────────────────  ─────────────────
[PM]
列 P0 4 widget       對齊客戶 use case   驗證 wedge thesis
描述 use case        (real demo)         調整 catalog

[Design]
抓既有 design       畫 P0 4 widget      畫 P1 4 widget
tokens              + Storybook hookup

[RD]
選 chart library    寫 P0 schema +       寫 P1 widget
建 widgets/         component + registry  + 整合 backend
資料夾結構

[Prompt Eng]
讀 widget-catalog   寫 system prompt     few-shot 調優
熟悉 LLM tool API   接 LLM API          測 9 個 scenario
```

**關鍵**：不要等 design 把 8 個都畫完才開始 RD。Design / RD / Prompt Eng 三條線**並行**，靠 Zod schema 對齊。

---

## 7. RD 實作 Checklist（每個 widget）

- [ ] Zod schema 定義（`schemas/widget-name.ts`）
- [ ] React/Vue component（`components/WidgetName.tsx`）
- [ ] Props type 從 `z.infer<>` 來
- [ ] Storybook story（4-6 種 input 變化，含 edge case）
- [ ] Loading skeleton 樣式
- [ ] Error state（schema 不合法時的 fallback）
- [ ] Responsive（手機壞掉的話至少不要爆版）
- [ ] 註冊到 `WIDGET_REGISTRY`

---

## 8. Prompt Engineering Checklist

- [ ] System prompt 列出可用 widget（用 `widget-catalog.md` 內容）
- [ ] LLM tool spec 從 `LLM_TOOLS` 自動產出（不手寫）
- [ ] Few-shot examples：9 個 scenario 各 1 組（user query → tool calls）
- [ ] Closed-set rule：明確告訴 LLM「只能用 catalog 裡的 widget，不能發明」
- [ ] Combo rules：限定 dashboard 上限 widget 數（建議 ≤ 6）
- [ ] Validation：LLM 回傳的每個 widget JSON 都過 Zod，壞了重 prompt

---

## 9. Common Pitfalls

### 設計面
- ❌ **等 design 寫 100 頁 design system 才開始** — wedge PoC 6-8 週要見驗證，等不到
- ❌ **重寫 design guideline，不對齊既有 EnGenius Cloud GUI** — 兩套設計打架
- ❌ **Design 跟 RD 不並行** — 卡在 waterfall，blocked

### 架構面
- ❌ **沒有 closed set，讓 LLM 自由生成任意 widget** — hallucination + 渲染失敗
- ❌ **先挑 UI library，schema 倒著寫** — schema 被綁架，未來換 library 痛苦
- ❌ **沒有 Zod runtime check** — LLM 偶爾吐壞 JSON，前端炸掉
- ❌ **Schema 寫太複雜（80 個欄位 / 4 層巢狀）** — LLM 生不出來
- ❌ **手寫兩份（schema + tool spec）** — 維護災難，一定會 drift

### 範圍面
- ❌ **第一版做 11 個 widget** — 太貪心，先做 P0 4 個跑通整個 loop，再依 P1 / P2 漸進
- ❌ **沒定 widget 上限** — dashboard 一次塞 12 個 widget，使用者看不懂

---

## 10. 第一週交付物

完成這些就算 setup 完成：

| 交付物 | Owner | 形式 |
|---|---|---|
| `design-tokens.md`（從既有 GUI 抓） | Design | Markdown / Figma frame |
| `widgets/schemas/kpi-card.ts` | RD | TypeScript + Zod |
| `widgets/schemas/time-series.ts` | RD | TypeScript + Zod |
| `widgets/registry.ts`（含 KPI + Time Series） | RD | TypeScript |
| 一個 KPI Card 在 Storybook 跑起來 | RD + Design | Storybook URL |
| LLM 接 1 個 tool（render_kpi_card）成功 render | Prompt Eng + RD | 影片 / GIF |

第一週通了，後面 widget 就是複製貼上。

---

## 11. 相關文件

- [widget-catalog.md](./widget-catalog.md) — 11 個 widget 的詳細規格（給人看的版本）
- [prompt-templates.md](./prompt-templates.md) — LLM system prompt + 11 個 tool defs + few-shot examples
- [../dashboard-builder-implementation.html](../dashboard-builder-implementation.html) — 工程實作指南（4-tab 互動頁）
- [../dashboard-builder-demo.html](../dashboard-builder-demo.html) — 9 個 scenario 的互動 demo

---

## 12. Open Questions（要在 kickoff 前定）

- [ ] 既有 EnGenius Cloud 用的 UI / chart library 是哪些？（決定 reuse vs 新選）
- [ ] Stack：React / Vue? Tailwind? CSS-in-JS?
- [ ] LLM 走哪家 API？（Anthropic / OpenAI / 自架）
- [ ] Widget 的 data 從哪打？（API gateway / 直連 SQL / cache layer）
- [ ] Dashboard JSON spec 存在哪？（DB / 使用者本地 / cloud workspace）
- [ ] 多語：widget label 要不要 i18n key 化？
- [ ] 客製化：使用者能改 widget title / 顏色嗎？（v1 建議不開）
