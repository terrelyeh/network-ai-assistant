# Widget: `alert`

A banner that surfaces a single high-priority message (license about to expire, audit finding, incident, etc.).

## When to use

- Top of a dashboard, before KPI cards
- A single sentence (≤120 chars) that gives the "headline" — what's the one thing the viewer should know?
- Body text can be static OR computed dynamically from live data

## When NOT to use

- For multiple messages (use a list of alerts? — not currently supported; instead make a `table` of issues)
- For ongoing diagnostics (use `card` with rich body)

## Config schema

```jsonc
{
  "widget": "alert",
  "id": "license-crit",              // optional; used for cross-widget targeting
  "severity": "critical",            // one of: "critical" | "warning" | "info" | "success"
  "title": "License 全面過期警示",       // required, string
  "body": "靜態文字",                  // optional — static body
  "body_compute": "license_summary", // optional — name of compute fn registered in computeFns map; takes (data) → string
  "icon": "!"                        // optional — single-char icon override (default "!")
}
```

`body` and `body_compute` are mutually exclusive. If both, `body_compute` wins.

## Compute function signature

```js
window.computeFns.my_alert_body = (data, config) => {
  // data: { <alias>: <fetched JSON> ... }
  return `Some computed string based on ${data.inventory.device_candidates.length} devices`;
};
```

## Visual

- 14px rounded bar, color-coded by severity
- 22px circular icon on left, white "!" inside
- Bold title + secondary body text
- Width: full-bleed inside `.db-wrap`

## Example

```json
{
  "widget": "alert",
  "severity": "warning",
  "title": "離職風險警示",
  "body_compute": "stale_summary"
}
```

## Visual reference

`canvas-org-health-v2-*.html` (critical) · `canvas-offboarding-audit-*.html` (warning)
