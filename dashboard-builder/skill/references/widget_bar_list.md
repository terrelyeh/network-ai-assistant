# Widget: `bar_list`

Horizontal bar chart for showing composition / distribution across discrete categories.

## When to use

- Showing breakdown by category (device type, license status, role, etc.)
- 2-12 bars (more than that becomes hard to read)
- Multiple groups can stack (e.g. "type" group above "license status" group)

## When NOT to use

- Time-series / trend (use `timeline`)
- Single number (use `kpi_grid`)
- Detailed records (use `table`)
- Hierarchical (use `topology_tree`)

## Config schema

```jsonc
{
  "widget": "bar_list",
  "id": "composition",
  "title": "Composition",
  "meta": "type · license",       // shown in card-hdr right
  "groups": [
    {
      "compute": "device_type_bars",       // OR "items": [...] for static
      "total_compute": "device_total"      // used to compute % width (% = value / total * 100)
    },
    {
      "compute": "license_status_bars",
      "total_compute": "device_total"
    }
  ]
}
```

Groups beyond the first are visually separated by a top border + extra spacing.

## Compute function signatures

```js
// Items compute: returns array of {label, value, color}
window.computeFns.device_type_bars = (data) => {
  const inv = data.inventory.device_candidates;
  const types = inv.reduce((m,d)=>{m[d.type]=(m[d.type]||0)+1;return m;},{});
  const colorMap = { ap: '', switch: 'warn', gateway: 'ok' };
  return Object.entries(types).map(([t,c]) => ({
    label: t.toUpperCase(),
    value: c,
    color: colorMap[t]  // see below
  }));
};

// Total compute: returns a single number (used for % calculation)
window.computeFns.device_total = (data) => data.inventory.device_candidates.length;
```

## Color names

| color | rendered as |
|---|---|
| (empty / unset) | `--brand` (deep blue) |
| `crit` | `--critical` (red) |
| `warn` | `--warning` (amber) |
| `ok` | `--success` (green) |

## Visual

- Each row: 110px label + flexible track + 32px right-aligned value
- Track is 8px tall, 4px rounded
- Fill animates from 0 → target width on initial render (0.6s ease)

## Example: license overdue by org

```json
{
  "widget": "bar_list",
  "title": "Overdue by Org",
  "groups": [
    { "compute": "overdue_by_org_bars", "total_compute": "fleet_total" }
  ]
}
```

With compute_fn:

```js
computeFns.overdue_by_org_bars = (data) => {
  const all = data.topology.orgs.flatMap(o => o.devices.map(d => ({...d, org_name: o.org_name})));
  const by = {};
  all.filter(d => d.license_status === 'expired').forEach(d => {
    by[d.org_name] = (by[d.org_name] || 0) + 1;
  });
  return Object.entries(by).map(([org, count]) => ({ label: org, value: count, color: 'crit' }));
};
```

## Visual reference

`canvas-org-health-v2-*.html` (Composition) · `canvas-license-renewal-*.html` (Overdue by Org)
