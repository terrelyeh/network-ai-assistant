# Widget: `topology_tree`

Hierarchical tree showing Org → Network → Device structure across multiple orgs. RBAC-aware (shows 403/402 badges for blocked orgs).

## When to use

- Cross-org structural view (you have 2+ orgs and want to see their networks)
- Want to show "what's where" relationships
- Want to drill from high-level (org) down to specific device

## When NOT to use

- Single org / single network (use `table` or `bar_list`)
- Need geographic / physical topology (not supported; tree is logical only)
- Need to show LLDP/CDP device-to-device connections (not in current data scope)

## Config schema

```jsonc
{
  "widget": "topology_tree",
  "id": "topology",
  "title": "Network Topology · All Orgs",
  "data_source": "topology",            // path to topology JSON object (with `orgs` array)
  "device_table_target": "device-fleet" // optional: id of table widget to dispatch expand-row to
}
```

## Expected data shape

```jsonc
{
  "fetched_at": "2026-05-15T23:42:34",
  "orgs": [
    {
      "org_id": "...",
      "org_name": "Main_Org",
      "hv_status": "ok",        // "ok" | "forbidden" | "payment_required" | "not_found"
      "hv_error": "...",        // shown if hv_status != ok
      "inv_status": "ok",       // same enum; affects per-network "device list 受限"
      "inv_error": "...",
      "networks": [
        { "network_id": "...", "network_name": "Sec_Network", "name": "Sec_Network", ... }
      ],
      "devices": [
        { "device_id": "...", "name": "ECW230", "mac": "...", "model": "ECW230",
          "type": "ap", "network_id": "...", "license_status": "expired" }
      ]
    },
    // ... more orgs
  ]
}
```

This is produced by `prototype/scripts/build_topology.sh` (aggregates `hvs.get_hierarchy_views` + `org-devices.get_inventory` across all orgs).

## Cross-widget events

**Emits**:
- `table-expand-row` with `{ tableId: device_table_target, rowId: device.device_id }` when user clicks a device leaf

**Receives**: none

## Interactions

- Click org row → toggle expand/collapse its networks
- Click network row → toggle expand/collapse its devices
- Click device leaf → emit cross-widget event (table receives + expands matching row)

## Auto-expand behavior

On first render, the widget automatically expands:
1. The org with the most devices
2. All non-empty networks within that org

This makes the tree visually populated on load even if user doesn't touch it.

## RBAC badges

| `hv_status` | Badge shown |
|---|---|
| `ok` | (none) |
| `forbidden` | `403 RBAC` (red) |
| `payment_required` | `402 BASIC` (amber) |
| `not_found` | `404` (muted) |

When `hv_status !== "ok"`, the entire org sub-tree is replaced with "無法讀取此 org 的階層資料".
When `inv_status !== "ok"` but `hv_status === "ok"`, the network expands but device list shows "device list 受限".

## Visual

- 3-stat header above tree (Orgs accessible / Networks total + empty / Devices)
- Tree:
  - 🏢 Org rows: bold, 14px
  - 📡 Network rows: medium, dashed left guide
  - 📶/🔘/🛡️ Device leaves (AP/switch/gateway): smaller, indented
- Empty networks: 55% opacity + "(empty)" suffix
- Expired-license devices: red text

## Example

```json
{
  "widget": "topology_tree",
  "id": "topology",
  "title": "Network Topology · All Orgs",
  "data_source": "topology",
  "device_table_target": "device-fleet"
}
```

## Visual reference

`canvas-org-health-v2-*.html` — bottom section. Try clicking ECW230 → it scrolls back up + expands that row in Device Fleet.
