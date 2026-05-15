# Widget: `chip_strip`

A row of small dashed-outline tags. Used for "minor / overflow / contextual" lists that don't need a full table.

## When to use

- Showing names of "empty networks", "users without login", "unassigned devices"
- 0-30 short items (more than that is visual noise)
- Items don't need attributes, just identity

## When NOT to use

- For data with attributes (use `table`)
- For metrics (use `kpi_grid`)
- For comparisons (use `bar_list`)

## Config schema

```jsonc
{
  "widget": "chip_strip",
  "id": "empty-nets",
  "title": "Empty Networks",      // section label above the strip
  "compute": "empty_networks",    // OR "items": [{ "label": "...", "tooltip": "..." }]
  "empty_text": "全部 network 都有設備"  // shown when items.length === 0
}
```

## Compute function signature

```js
window.computeFns.empty_networks = (data) => {
  const inv = data.inventory.device_candidates;
  const hv = data.hierarchy.network_candidates;
  const usedNames = new Set(inv.map(d => d.network_name));
  return hv.filter(n => !usedNames.has(n.network_name))
    .map(n => ({ label: n.network_name, tooltip: n.network_id }));
};
```

Returns array of `{label: string, tooltip?: string}`.

## Visual

- Section label (11px uppercase grey above)
- Tags wrap as needed, 6px gap
- Each tag: dashed border, mono font, muted color
- Tooltip on hover (HTML `title` attribute)
- Empty state: shown when items.length === 0, plain grey text

## Example

```json
{
  "widget": "chip_strip",
  "title": "Never Logged In",
  "compute": "never_logged_in",
  "empty_text": "所有人都至少登入過一次"
}
```

## Visual reference

`canvas-org-health-v2-*.html` (Empty Networks · 7 tags) · `canvas-offboarding-audit-*.html` (empty state shown)
