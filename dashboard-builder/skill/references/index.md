# Widget Catalog · Quick Reference

10 widgets currently available. Each widget has its own detail page in this folder.

| Widget | One-liner | Best for | Detail |
|---|---|---|---|
| [`alert`](widget_alert.md) | Single high-priority banner | "Here's the one thing you need to know" | critical / warning / info / success |
| [`kpi_grid`](widget_kpi_grid.md) | 2-6 metric cards | "Current state at a glance" | Clickable cross-widget targets |
| [`table`](widget_table.md) | Filterable rows + expand for detail | "Show me records" | filters / expandable / row-click events |
| [`bar_list`](widget_bar_list.md) | Horizontal bars per category | "Distribution / composition" | grouped bars, severity colors |
| [`donut`](widget_donut.md) | SVG ring chart with center metric | "% of total" framing | hover sync, 2-6 segments |
| [`gauge`](widget_gauge.md) | Half-circle gauge with target | "Where are we on the scale?" | thresholds, delta vs target |
| [`chip_strip`](widget_chip_strip.md) | Dashed tags | "Minor list, no attributes" | empty-state aware |
| [`topology_tree`](widget_topology_tree.md) | Hierarchical org → net → device | "Cross-org structure" | RBAC-aware, click device → expand table row |
| [`timeline`](widget_timeline.md) | Dated items on horizontal axis | "When things happen / are due" | TODAY marker, severity by date |
| [`heatmap`](widget_heatmap.md) | 2D matrix with cell-intensity colors | "Hotspot in 2 dimensions" | palette options, hover tooltip |

## Future candidates (not built yet)

Add as scenarios demand. Each takes ~1 hour to build.

| Idea | When you'd add it | Blocker |
|---|---|---|
| `line_chart` | Continuous time-series trend | ❌ No historical API yet |
| `sparkline` | Inline mini-trend in table cells | Same as above |
| `donut` / `pie` | Composition with strong "100% of" framing | ✅ Buildable today |
| `heatmap` | 2D cross-tab (e.g. user × network access) | ✅ Buildable today |
| `map` (geographic) | Multi-site physical location | ❌ No lat/lon in data |
| `graph` / `network` | LLDP / CDP physical topology | ❌ Needs `subscribe_fdb_list` op |
| `gauge` | Single metric vs target | ✅ Buildable today |
| `cost_forecast` | $$ projection over time | Could compose from existing |

## Adding a new widget — checklist

1. Create `widgets/<name>.html` with `<style>`, `<template>` (optional), `<script>` blocks
2. In `<script>`, call `Dashboard.register('<name>', factory)` — factory returns `{render(data)}`
3. Use `var(--token)` for all colors / fonts / spacing (never hardcode)
4. If widget needs cross-widget events, use `bus.dispatch` / `bus.on`
5. Add `references/widget_<name>.md` (use existing as template)
6. Update this `index.md` table
7. Test by writing a spec that uses it; run `compose.py`

## Conventions

- All widgets read `data` snapshot supplied by runtime; never write to live-data
- All widgets are inert until `render(data)` is called
- All widgets render into the `el` passed to factory (a `<div data-widget-id="...">`)
- Severity vocabulary is fixed: `critical | warning | success | info` — don't invent new ones
