# Widget: `timeline`

Horizontal time-axis visualization. Each item gets a dot positioned by its date, severity-coded by past / near-future / far-future relative to TODAY.

## When to use

- Showing N dated events along a time axis (license expirations, scheduled maintenance, deployments)
- Want to visually compare "what's overdue" vs "what's coming up" vs "what's safe"
- Want a "TODAY" anchor for context

## When NOT to use

- For continuous time-series / trend (need data points at every interval — not supported, would need `line_chart` widget)
- For very dense data (50+ items at similar dates will cluster ugly)
- For categorical comparisons (use `bar_list`)

## Config schema

```jsonc
{
  "widget": "timeline",
  "id": "expiry-timeline",
  "title": "License Expiry Timeline",
  "compute": "licenses_for_timeline",        // OR "items": [{label, date_ms, severity?, sub?}]
  "warning_threshold_days": 90,              // optional: items expiring < N days from now get warning color
  "critical_label": "Overdue (action required)",  // legend label override
  "warning_label": "Expiring < 90d (plan renewal)",
  "success_label": "Active (safe)"
}
```

## Compute function signature

```js
window.computeFns.licenses_for_timeline = (data) => {
  const flatten = (data.topology.orgs || []).flatMap(o =>
    (o.devices || []).map(d => ({...d, org_name: o.org_name}))
  );
  return flatten.map(d => ({
    label: d.name,
    date_ms: d.expired_date,
    severity: null,         // null = auto-classify by date (past/near/future)
    sub: d.org_name         // shown in tooltip
  }));
};
```

Returns array of `{label: string, date_ms: number, severity?: string|null, sub?: string}`.

## Auto severity classification

When `item.severity` is null/undefined, the widget classifies based on date vs `now`:

| Condition | Severity |
|---|---|
| `date_ms < now` | `critical` (red — past/overdue) |
| `0 ≤ (date_ms - now) days < warning_threshold_days` | `warning` (amber — coming up soon) |
| else | `success` (green — safely in the future) |

Explicit `item.severity` always wins (use it when severity is independent of date — e.g. compliance audits).

## Visual

- Card-wrapped
- 130px tall canvas
- Horizontal track: 2px line, full width minus 4px padding
- "TODAY" marker: blue vertical line with "TODAY" label at top
- Year ticks: thin grey vertical lines + year label below
- Item dots: 14px circle, severity-colored, white border + drop shadow
- Cluster: when multiple items share the same date, shown as one larger (18px) dot with combined tooltip
- Hover dot: 1.4× scale, tooltip appears with label(s) + sub + date
- Label above each dot (truncated; cluster shows count like "10× ECW115")
- Legend below track: dots + counts per severity

## Date range auto-calculation

- Min/max from items + `now` (so TODAY is always in range)
- 8% padding on each side
- Year ticks auto-generated between min and max year

## Clustering behavior

Items grouped by `fmtDay(date_ms)` (YYYY-MM-DD). Same-day items collapse into one dot.

Tooltip shows up to 5 item labels, then "(+N)" suffix if more.

## Example: license expiry across orgs

```json
{
  "widget": "timeline",
  "title": "License Expiry Timeline",
  "compute": "licenses_for_timeline",
  "warning_threshold_days": 90
}
```

For our staging data: 10 Main_Org devices cluster at 2022-12-01 (red), 1 Vertical Demo gateway at 2031-04-08 (green), TODAY in 2026 in the middle.

## Visual reference

`canvas-license-renewal-*.html` — primary use case
