# Widget: `gauge`

Half-circle gauge showing a single metric vs a scale (and optional target). Half-donut visual with center value + side info panel.

## When to use

- Single key metric that's bounded (0-100%, 0-N, "fleet utilization %")
- Want to show progress toward a target
- Want a "speedometer" feel — "where are we on the scale?"

## When NOT to use

- For unbounded counts (use `kpi_grid`)
- For multiple metrics (use `kpi_grid` × N)
- For composition (use `donut` or `bar_list`)
- For time-axis (use `timeline`)

## Config schema

```jsonc
{
  "widget": "gauge",
  "id": "fleet-license-coverage",
  "title": "Fleet License Coverage",
  "value_compute": "active_license_pct",   // OR value_path
  "min": 0,
  "max": 100,
  "min_label": "0%",                        // tick label override (default = min)
  "max_label": "100%",
  "value_format": "percent",                // OR omit (raw value + unit)
  "unit": "%",
  "center_label": "Active",                 // shown below the value
  "target": 80,                             // optional target line
  "thresholds": {
    "critical_below": 30,                   // val ≤ 30 → critical
    "warning_below": 60,                    // val ≤ 60 → warning
    "ok_severity": "success"                // else → success
  },
  "info_title": "Fleet Coverage Health",
  "info_body_compute": "fleet_coverage_narrative",  // OR info_body: "static text"
  "severity": "critical"                    // optional explicit override (skips thresholds)
}
```

## Compute function signatures

```js
// Value
window.computeFns.active_license_pct = (data) => {
  const inv = data.inventory.device_candidates;
  const active = inv.filter(d => d.license_status === 'active').length;
  return inv.length > 0 ? (active / inv.length * 100).toFixed(0) : 0;
};

// Side narrative
window.computeFns.fleet_coverage_narrative = (data) => {
  const inv = data.inventory.device_candidates;
  const exp = inv.filter(d => d.license_status === 'expired').length;
  return `${exp} 台設備需要 license 續約。Target 80% 代表至少 8 成 fleet 應隨時保持活躍 license。`;
};
```

## Threshold logic

When `severity` is omitted, the widget classifies based on value vs thresholds:

| Threshold key | Triggers when |
|---|---|
| `critical_above` | val ≥ this → critical color (red) |
| `warning_above` | val ≥ this → warning color (amber) |
| `critical_below` | val ≤ this → critical color (red) |
| `warning_below` | val ≤ this → warning color (amber) |
| (none match) | `ok_severity` value (default `success`) |

Use `_below` thresholds for metrics where LOW = BAD (e.g. license coverage, uptime).
Use `_above` thresholds for metrics where HIGH = BAD (e.g. CPU load, error rate).

## Visual

- 200×130 SVG with a half-circle path (semicircle gauge)
- Stroke fills clockwise from left → right as value rises
- Color comes from severity classification
- Center: big value + small label below
- Min/max tick labels at bottom corners
- Right panel: optional info title + body + delta vs target (with color)

## Example: fleet license coverage

```json
{
  "widget": "gauge",
  "title": "License Coverage",
  "value_compute": "active_license_pct",
  "min": 0,
  "max": 100,
  "value_format": "percent",
  "center_label": "Active",
  "target": 80,
  "thresholds": {
    "critical_below": 30,
    "warning_below": 70
  },
  "info_title": "Fleet Coverage Health",
  "info_body_compute": "fleet_coverage_narrative"
}
```

## Visual reference

`canvas-cross-org-reallocation-*.html` — primary use case
