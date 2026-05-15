---
name: dashboard-builder
description: >
  Compose a live, interactive HTML dashboard from a widget-based spec JSON.
  Use this skill when you have already gathered data via data skills (init-orgs / hvs / org-devices / org-licenses / team-members / networks etc.) and want to render it as a stateful canvas with auto-poll, filters, and drill-down.
  Output is a single .html file that polls live-data/*.json every 5 seconds.
---

# Dashboard Builder

This skill turns a small spec JSON into a polished, interactive HTML dashboard. Visual consistency is guaranteed by sharing a single design system (theme/tokens.css + base.css) and a widget library (widgets/*.html). Each widget is self-contained: HTML partial + JS module that registers itself on a shared `Dashboard` runtime.

## Quick Reference

| Task | How |
|---|---|
| Render a dashboard | `python scripts/compose.py --spec path/to/spec.json --out canvas-<topic>-<TS>.html` |
| List available widgets | `ls widgets/*.html` |
| Read widget contract | One file per widget: `references/widget_<name>.md` |
| See a working spec | `examples/org-health.spec.json` |

## Spec JSON Schema (informal)

```jsonc
{
  "title": "string",                 // shown in header
  "subtitle": "string",              // optional
  "live_data": {                     // map of alias → relative path
    "<alias>": "live-data/<file>.json"
  },
  "sections": [
    {
      "widget": "<widget_name>",     // must match a file in widgets/
      "id": "string",                // optional; used by scroll/flash targets
      // ... widget-specific config; see references/widget_<name>.md
    }
  ],
  "footer": {                        // optional
    "ops_used": ["get_inventory", "get_hierarchy_views"],
    "auto_refresh_seconds": 5
  }
}
```

## Available Widgets

| Widget | Purpose | Reference |
|---|---|---|
| `alert` | Banner (critical/warning/info/success) | references/widget_alert.md |
| `kpi_grid` | 2-6 KPI cards in a row, optional clickable | references/widget_kpi_grid.md |
| `card` | Generic surface with header + chips + content slot | references/widget_card.md |
| `table` | Tabular data with filter chips + expandable rows | references/widget_table.md |
| `bar_list` | Compositional bar chart (horizontal bars w/ labels) | references/widget_bar_list.md |
| `chip_strip` | List of small tags (e.g. empty networks) | references/widget_chip_strip.md |
| `topology_tree` | Hierarchical org → network → device tree | references/widget_topology_tree.md |

## Flow Modules

### F0. Validate spec

1. Spec MUST contain `title` and non-empty `sections`.
2. Every `widget` value MUST exist as a file under `widgets/`.
3. Every `data_source` (or `value_path`) MUST refer to an alias declared in `live_data`.
4. If validation fails, stop and report the offending section to the caller.

### F1. Assemble HTML

1. Read `theme/tokens.css` + `theme/base.css` → inline into single `<style>` block.
2. Read `runtime/runtime.js` → inline into single `<script>` block (before widget scripts).
3. For each section, read `widgets/<name>.html`, extract its `<style>` / `<template>` / `<script>` blocks, append to the corresponding bundle, substituting `{{config}}` placeholders.
4. Emit a single `<body>` with `<header>`, ordered widget mount points, and a `<footer>`.

### F2. Wire runtime

1. Generated HTML includes `Dashboard.init({spec, live_data, sections})` call at end of body.
2. Runtime starts a `setInterval(fetchAll, 5000)` loop and calls each widget's `render(data)` on every tick.
3. Runtime exposes `Dashboard.bus` for cross-widget events (e.g. tree node click → table filter).

### F3. Manifest entry (caller's responsibility, not this skill)

After compose, the caller (Claude Code) should:
- Append entry to `prototype/generated-manifest.json` so `generated-log.html` shows it
- Print the relative path of the output file

## Constraints

- **C1** — All visual styling MUST come from `theme/`. Widgets MUST NOT hardcode colors / fonts / spacing in their `<style>` block — use `var(--token)`.
- **C2** — Widgets MUST be self-contained; one widget cannot reference another widget's DOM directly. Communicate via `Dashboard.bus`.
- **C3** — Data binding is unidirectional: widget reads from `data` snapshot supplied by runtime; widget never writes to live-data files.
- **C4** — Auto-poll interval is fixed at 5 seconds. Do not make it configurable in V1.
- **C5** — Output HTML is self-contained (no external runtime fetch); only fetches its own `live-data/*.json` files.
