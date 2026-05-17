- method: POST
- path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/devices

Assign one or more inventory devices to a target network.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |
| hvId | string | Hierarchy view id from `get_hierarchy_views`. |
| networkId | string | Target network id from `get_hierarchy_views.networks[].id`. |

### Query Parameters

(EMPTY)

### Request Body Example

```json
[
  {
    "id": "ab9d5b054e4352f18f2146cdbcbe5c03"
  },
  {
    "id": "ab9d5b054e4352f18f2146cdbcbe5c04",
    "is_config_overwrite_pending": true
  }
]
```

### Request Body Item Schema

| Field | Type | Required | Description |
|---|---|---|---|
| id | string | true | Device id from org inventory. |
| is_config_overwrite_pending | boolean | false | Optional overwrite flag. |
| is_gateway_ha_backup_unit_added | boolean | false | Optional gateway HA backup flag. |

### Response Body Example

```json
[
  {
    "id": "ab9d5b054e4352f18f2146cdbcbe5c03",
    "code": 200,
    "message": "OK",
    "license_status": "active"
  }
]
```

### Response Body Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | Device id. |
| code | integer | Per-device result code. |
| message | string | Per-device result message. |
| expired_date | integer | License expiry timestamp when available. |
| license_status | string | Resulting license status when available. |

### Usage Notes

- Device ids must come from `get_inventory.devices[].id`.
- Use this API for assign-to-network flow, not for inventory registration.
