# Widget: `kpi_grid`

A row of 2–6 KPI cards at the top of a dashboard, each showing one headline metric. Cards can be clicked to scroll/flash a target widget.

## When to use

- 2nd from top, right after `alert`
- 3-5 metrics that capture the dashboard's main message
- Each card answers "what is the current number?" — not trend (use `timeline` for trend)

## When NOT to use

- For more than 6 metrics (too dense; pick the most important)
- For long-form text (use `alert`)
- For comparison over time (use `timeline`)

## Config schema

```jsonc
{
  "widget": "kpi_grid",
  "id": "kpis",
  "items": [
    {
      "label": "Devices",                    // required
      "severity": "critical",                // optional: "critical" | "warning" | "success" | (none = neutral)
      "value_path": "inventory.device_candidates.length",   // EITHER path...
      "value_compute": "expired_count",      // ...OR compute function name
      "sub": "9 ap · 1 switch",              // EITHER static subtext...
      "sub_compute": "device_type_breakdown",// ...OR computed subtext
      "clickable": {                         // optional — turn card into a button
        "target": "device-fleet"             // id of another widget to scrollIntoView + flash
      }
    },
    // ... more items (2-6 total)
  ]
}
```

## Compute function signature

```js
window.computeFns.my_kpi_value = (data, item) => {
  return data.inventory.device_candidates.filter(d => d.license_status === 'expired').length;
};
```

Returns a string or number. The value is text-substituted into the `.val` element.

## Cross-widget event

When a clickable KPI is clicked, two things happen:
1. The runtime scrolls + flashes the target widget (`clickable.target` matches `data-widget-id`)
2. The event `kpi-click` is dispatched on the bus with `{ item, target, action }`

## Visual

- Grid with `repeat(N, 1fr)` columns (N = number of items)
- Each card: 18px padding, 36px big number, 12px subtitle
- Severity tinted background + colored value (critical = red gradient, warning = amber border)
- Clickable cards: hover lifts by 2px + shows ↗ icon top-right

## Example

```json
{
  "widget": "kpi_grid",
  "items": [
    { "label": "Total Members", "value_path": "memberships.org_member_candidates.length" },
    { "label": "Stale", "severity": "warning", "value_compute": "stale_count",
      "sub_compute": "stale_subtext", "clickable": { "target": "stale-members" } }
  ]
}
```

## Visual reference

All current canvases use this widget.
