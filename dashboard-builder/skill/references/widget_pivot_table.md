# `pivot_table` widget

2D cross-tabulation: rows × columns, each cell shows `value` (+ optional `sub` and `severity`).

## When to use

- "Type × Org" device matrix
- "Severity × Day" alert pivot
- Any question of the form "X grouped by both A and B"

## When **not** to use

- Single dimension distribution → use `bar_list` or `donut`
- 2D continuous data with intensity only → use `heatmap`
- Long flat list with multiple attributes → use `table`

## Spec config

```jsonc
{
  "widget": "pivot_table",
  "id": "type-by-org",
  "title": "類型 × Org 交叉矩陣",
  "meta": "optional subtitle",
  "compute": "type_by_org_pivot",  // computeFns key
  "show_totals": "both",           // "both" | "rows" | "cols" | "none"
  "heatmap": true,                 // optional — color cells by intensity
  "row_header": "Org",             // optional column-0 label
  "row_total_label": "合計",       // optional
  "col_total_label": "合計"        // optional
}
```

## Compute function shape

The `compute` function (declared in `spec.compute_fns` or inherited) must return:

```js
{
  rows: [
    { key: 'claudia', label: 'Claudia' },
    { key: 'chanel',  label: 'Chanel' }
  ],
  cols: [
    { key: 'camera', label: 'Camera' },
    { key: 'ap',     label: 'AP' }
  ],
  cells: {
    claudia: {
      camera: { value: 63, sub: '0/63', severity: 'crit' },
      ap:     { value: 7,  sub: '3/4',  severity: 'warn' }
    },
    chanel: {
      camera: { value: 1, sub: '0/1', severity: 'crit' },
      ap:     { value: 7, sub: '6/1', severity: 'ok' }
    }
  }
}
```

### Cell fields

| Field | Type | Notes |
|---|---|---|
| `value` | number | Primary cell value (large, bold) |
| `sub` | string | Optional secondary text (e.g. `"3/4"` for active/expired) |
| `severity` | `"crit"` / `"warn"` / `"ok"` / `"info"` | Color of the `sub` text |
| `heat` | number 0-1 | Optional override of heatmap intensity |

Empty cell (no `value` key, or value=null) renders as `·` muted.

## Heatmap mode

When `"heatmap": true`, cells get a background tint based on `value / maxValue`:
- ≥ 0.75 → critical-red strong
- ≥ 0.50 → critical-red mid
- ≥ 0.25 → critical-red light
- > 0    → critical-red faint
- = 0    → no tint

## Example: V2 dashboard's missing 4th widget

This is exactly the widget that the hand-rolled V1 had but compose.py V2 lacked. Now V2 can match V1 density:

```jsonc
{
  "widget": "pivot_table",
  "id": "type-org-matrix",
  "title": "類型 × Org 交叉矩陣",
  "compute": "type_org_matrix",
  "heatmap": true,
  "row_header": "Org",
  "show_totals": "both"
}
```

With a `compute_fns`:

```js
window.computeFns.type_org_matrix = (data) => {
  const inv = data.dist?.orgs || [];
  const cols = [/* unique types from inv */];
  return {
    rows: inv.map(o => ({ key: o.id, label: o.name })),
    cols,
    cells: Object.fromEntries(inv.map(o => [
      o.id,
      Object.fromEntries(cols.map(c => {
        const total = o.devices.filter(d => d.type === c.key).length;
        const expired = o.devices.filter(d => d.type === c.key && d.license_status === 'expired').length;
        return [c.key, { value: total, sub: `${total-expired}/${expired}`, severity: expired ? 'crit' : 'ok' }];
      }))
    ]))
  };
};
```
