# Widget: `table`

A tabular widget with filter chips, expandable rows (for detail), sort, and cross-widget event handling. The workhorse of most dashboards.

## When to use

- Listing 5-50 records (devices, members, licenses, etc.)
- Need to filter by category (type, status, role)
- Need progressive disclosure (collapsed by default, expand for detail)

## When NOT to use

- More than 50 rows without good filters (will overwhelm; paginate or summarize first)
- For aggregate / chart data (use `bar_list`, `timeline`)
- For hierarchical data (use `topology_tree`)

## Config schema

```jsonc
{
  "widget": "table",
  "id": "device-fleet",            // recommended — enables cross-widget targeting
  "title": "Device Fleet",
  "data_source": "inventory.device_candidates", // path into live-data
  "row_id_field": "device_id",     // field used as stable row id; required for expand state
  "sort_by": { "field": "last_login_time", "dir": "asc" }, // optional, default no sort
  "meta_template": "${count} devices",  // shown in card-hdr right side; ${count} = total
  "filters": [                     // optional — first filter is default active
    { "label": "All", "filter": "all" },              // no-op pass-through
    { "label": "AP", "filter": "type:ap" },           // field:value equality
    { "label": "Expired only", "filter": "license_status:expired" },
    { "label": "Stale (1y+)", "filter": "stale" }    // special: requires last_login_time field
  ],
  "columns": [
    { "label": "Name", "field": "name",
      "render": "name_with_sub", "sub_field": "mac" },  // 2-line cell: bold name + mono sub
    { "label": "Network", "field": "network_name",
      "render": "network_or_unassigned" },              // shows pill if value missing
    { "label": "Model", "field": "model", "cls": "mono" },
    { "label": "Type", "field": "type", "render": "type_chip" },
    { "label": "License", "field": "license_status", "render": "license_pill" },
    { "label": "Last Login", "field": "last_login_time", "render": "date" },
    { "label": "Risk", "field": "last_login_time", "render": "risk_pill" },
    { "label": "Role", "field": "org_role", "render": "role_pill" },
    { "label": "Networks", "field": "networks", "render": "count", "align": "right" },
    { "label": "Email", "field": "email", "render": "mono_ellipsis" }
  ],
  "expandable_rows": true,
  "detail_fields": [               // shown in expanded panel below the row
    { "label": "Device ID", "field": "device_id" },
    { "label": "MAC", "field": "mac" },
    { "label": "License Type", "field": "license_type", "large": true },  // sans-serif font
    { "label": "Registered", "field": "registered_time", "render": "datetime" },
    { "label": "Network ID", "field": "network_id", "full_width": true }, // spans all columns
    { "label": "Network Access", "field": "networks",
      "render": "network_list", "full_width": true, "large": true }
  ]
}
```

## Built-in column renderers

| render | shows | requires |
|---|---|---|
| `name_with_sub` | bold name + mono sub-line | `sub_field` |
| `network_or_unassigned` | value or "unassigned" pill | — |
| `type_chip` | colored dot + UPPERCASE type | — |
| `license_pill` | expired (red) / active (green) / muted pill | — |
| `role_pill` | admin (blue) / viewer (muted) / other (warning) | — |
| `risk_pill` | days-since-login → pill (never/2y stale/1y stale/quiet/active) | `last_login_time` field |
| `date` | YYYY-MM-DD mono | timestamp ms |
| `count` | array length (right-aligned) | — |
| `mono_ellipsis` | mono text, truncated | — |
| (none) + `cls: "mono"` | plain mono text | — |
| (none) | plain text | — |

## Detail field renderers

| render | shows |
|---|---|
| (default) | mono small |
| `large` (flag) | sans-serif normal size |
| `datetime` | YYYY-MM-DD HH:MM mono |
| `date` | YYYY-MM-DD mono |
| `network_list` | each network as a pill, role suffix |
| `full_width` (flag) | spans all detail-grid columns |

## Filter syntax

- `"all"` — pass-through
- `"<field>:<value>"` — strict equality on row[field] === value
- `"stale"` — special: `daysSince(row.last_login_time) > 365`

To add new filter types, extend `passesFilter()` in `widgets/table.html` (or use compute_fns for pre-filtering).

## Cross-widget events

**Receives** (from any other widget):
- `table-expand-row` with `{ tableId, rowId }` — opens that row, scrolls + flashes it, resets filter to first chip if row isn't currently visible

**Emits**: none currently.

Typical pair: `topology_tree` dispatches `table-expand-row` when user clicks a device leaf, this table expands the matching row.

## Visual

- Card-wrapped (white surface, 14px radius)
- Header: title + right-aligned meta
- Filter chips row (pills, first is active by default)
- Standard table with hover, alt-row stripe, severity pills
- Expanded row: light surface background, 14px padding, grid of label/value pairs

## Example: members table with stale-only default

```json
{
  "widget": "table",
  "id": "stale-members",
  "title": "Stale Members · 應立即檢視",
  "data_source": "memberships.org_member_candidates",
  "row_id_field": "user_id",
  "sort_by": { "field": "last_login_time", "dir": "asc" },
  "filters": [
    { "label": "Stale (1y+)", "filter": "stale" },
    { "label": "Admins", "filter": "org_role:admin" },
    { "label": "All", "filter": "all" }
  ],
  "columns": [...],
  "expandable_rows": true,
  "detail_fields": [...]
}
```

## Visual reference

`canvas-org-health-v2-*.html` (devices + members) · `canvas-offboarding-audit-*.html` (stale-only + all)
