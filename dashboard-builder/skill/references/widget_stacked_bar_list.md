# `stacked_bar_list` widget

Horizontal bars, one per row, each bar split into multiple severity-colored segments. Bar widths scaled to the global max so cross-row comparison is accurate.

## When to use

- **Per-org Active/Expired/Other** breakdown in a single comparable bar
- Per-region Pass/Fail/Skipped test result
- Per-month Closed/Open/Reopened ticket counts

## When **not** to use

- Single value per row → use `bar_list`
- Distribution of one quantity → use `donut`
- Pivot data with multiple dimensions → use `pivot_table`

## Spec config

```jsonc
{
  "widget": "stacked_bar_list",
  "id": "org-license-mix",
  "title": "各 Org 設備數（Active vs Expired vs Other）",
  "meta": "optional subtitle",
  "compute": "org_license_stack",  // computeFns key
  "sort_by_total": true             // optional — default true, sort descending
}
```

## Compute function shape

```js
{
  rows: [
    {
      label: 'Claudia',
      // total optional — auto-computed from segments if absent
      segments: [
        { value: 11, severity: 'ok',   label: 'Active' },
        { value: 74, severity: 'crit', label: 'Expired' },
        { value: 1,  severity: 'muted', label: 'Other' }
      ]
    },
    {
      label: 'Chanel',
      segments: [
        { value: 20, severity: 'ok',   label: 'Active' },
        { value: 3,  severity: 'crit', label: 'Expired' },
        { value: 7,  severity: 'muted', label: 'Other' }
      ]
    }
  ],
  legend: [
    { label: 'Active',  severity: 'ok' },
    { label: 'Expired', severity: 'crit' },
    { label: 'Other',   severity: 'muted' }
  ]
}
```

### Severity colors

| Severity | Color | Use for |
|---|---|---|
| `ok` | green | Healthy / passing / current |
| `warn` | amber | Warning / nearing limit |
| `crit` | red | Critical / failed / expired |
| `info` | blue | Informational segment |
| `brand` | orange | Brand-highlighted segment |
| `muted` | gray | Other / unknown / inactive |

## Example: replacing 2-separate-bar_list approach

When the V2 compose.py dashboard had 2 separate `bar_list` widgets (one for Active up, one for Expired down), it could be replaced by a single `stacked_bar_list`:

```jsonc
{
  "widget": "stacked_bar_list",
  "id": "org-mix",
  "title": "各 Org License 狀態（Active / Expired / Other）",
  "compute": "org_license_stack",
  "sort_by_total": true
}
```

→ Same data, half the vertical space, easier cross-org comparison.

## Behavior

- Bar track width = `(row.total / globalMax) * 100%`, so rows with fewer items show shorter bars (easier visual comparison)
- Within each track, segments are sized by their share of `row.total`
- Hover on segment dims to 0.7 opacity (subtle, no scale animation)
- Empty rows render `<div class="empty">No data</div>`
