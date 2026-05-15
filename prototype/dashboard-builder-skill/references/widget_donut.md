# Widget: `donut`

SVG ring chart showing composition / proportion. Center shows a primary metric (total, percentage). Hover synchronization between legend and segments.

## When to use

- Show composition with strong "% of total" framing (e.g. accessible vs blocked orgs, license type mix)
- 2-6 segments (more than that = unreadable thin slices)
- Want a strong central headline number

## When NOT to use

- For absolute counts where total isn't meaningful (use `bar_list`)
- For >6 segments (use `bar_list`)
- For time-based composition (use `timeline` + grouping)

## Config schema

```jsonc
{
  "widget": "donut",
  "id": "org-access-mix",
  "title": "Orgs by Access Level",
  "compute": "org_access_segments",        // returns [{label, value, severity?}, ...]
  "center_value_compute": "total_orgs",    // OR center_value_path: "topology.orgs.length"
  "center_label": "Orgs"
}
```

## Compute function signature

```js
window.computeFns.org_access_segments = (data) => {
  const orgs = data.topology.orgs || [];
  return [
    { label: 'Fully Accessible', value: orgs.filter(o => o.hv_status === 'ok' && o.inv_status === 'ok').length, severity: 'success' },
    { label: 'HV ok, Inv blocked', value: orgs.filter(o => o.hv_status === 'ok' && o.inv_status !== 'ok').length, severity: 'warning' },
    { label: 'Fully Blocked', value: orgs.filter(o => o.hv_status !== 'ok').length, severity: 'critical' }
  ];
};
```

Returns `[{label, value, severity?, color?}]`. Either `severity` (critical/warning/success/info/brand/muted) or `color` (same enum) selects the stroke color.

## Severity / color values

| key | rendered as |
|---|---|
| `brand` (default) | EG brand orange |
| `critical` | red |
| `warning` | amber |
| `success` | green |
| `info` | blue |
| `muted` | grey |

## Interactions

- Hover a legend row → highlights matching segment, dims others
- Hover a segment → highlights it, dims others
- No click action by default (donut is informational)

## Visual

- 200×200 SVG, grid: 220px donut + flex legend
- Ring thickness: 28 units (out of 100 viewbox)
- Background ring: muted surface-2 (shows "remaining" if segments don't sum to viewable total)
- Center: 28px bold number + 10px uppercase label
- Legend: swatch + label + value + percentage (right-aligned)

## Example: orgs by access level

```json
{
  "widget": "donut",
  "title": "Orgs by Access",
  "compute": "org_access_segments",
  "center_value_path": "topology.orgs.length",
  "center_label": "Orgs"
}
```

## Visual reference

`canvas-multi-org-governance-*.html` — primary use case
