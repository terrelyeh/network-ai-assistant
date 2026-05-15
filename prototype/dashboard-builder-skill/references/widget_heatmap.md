# Widget: `heatmap`

2D matrix grid where each cell intensity = value. Used for cross-tab summaries (org × type, user × network, weekday × hour).

## When to use

- 2 categorical dimensions × 1 numeric metric
- Want to spot patterns / hotspots (where is the concentration?)
- Want at-a-glance "no data here" / "lots of data there" visual

## When NOT to use

- For continuous data without natural bins (use `bar_list`)
- For >15 × >15 cells (too dense to read; consider aggregating)
- For single-dimension data (use `bar_list`)

## Config schema

```jsonc
{
  "widget": "heatmap",
  "id": "device-by-org-type",
  "title": "Devices by Org × Type",
  "compute": "device_by_org_and_type",      // returns {rows, cols, cells}
  "palette": "brand",                       // "brand" | "critical" | "warning" | "success" | "info"
  "cell_format": "raw",                     // "raw" | "percent"
  "cell_unit": "",                          // suffix added in tooltip
  "legend_min": "0",
  "legend_max": "more"
}
```

## Compute function signature

```js
window.computeFns.device_by_org_and_type = (data) => {
  const orgs = data.topology.orgs;
  const types = ['ap', 'switch', 'gateway'];
  return {
    rows: orgs.map(o => o.org_name),
    cols: types.map(t => t.toUpperCase()),
    cells: orgs.map(o => types.map(t => o.devices.filter(d => d.type === t).length))
  };
};
```

Returns `{rows: string[], cols: string[], cells: number[][]}` — `cells[ri][ci]` is value at row `ri`, col `ci`.

- `null` or `0` → cell shown as muted "·"
- Positive numbers → cell colored by intensity (light → dark within palette)

## Palette options

| Palette | When to use |
|---|---|
| `brand` (default) | General — orange family |
| `critical` | Where high = bad (errors, incidents, outages) |
| `warning` | Where high = needs-attention (stale, near-expiry) |
| `success` | Where high = good (uptime, coverage) |
| `info` | Where neutral / informational |

## Visual

- Grid: row-header column + N data columns
- Each cell: 34px tall, value-colored background
- Hover: cell scales up 1.08× with tooltip showing "Row × Col: Value"
- Empty cells: muted "·" character
- Bottom legend: scale gradient + min/max labels

## Example: cross-org × device type

```json
{
  "widget": "heatmap",
  "title": "Fleet Composition · Org × Device Type",
  "compute": "device_by_org_and_type",
  "palette": "brand",
  "legend_min": "0",
  "legend_max": "all"
}
```

For our staging data:
- Rows: 5 orgs (Main_Org / terrel / Vertical Demo / ann-AP / Gordon)
- Cols: 3 types (AP / SWITCH / GATEWAY)
- Most cells empty; Main_Org has [9, 1, 0]; Vertical Demo has [0, 0, 1]

## Visual reference

`canvas-cross-org-reallocation-*.html` — primary use case
