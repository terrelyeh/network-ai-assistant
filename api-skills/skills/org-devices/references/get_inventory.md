- method: GET
- path: /orgs/{orgId}/inventory

Return devices in organization inventory.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |

### Query Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| from | integer | false | 0 | Pagination start index. |
| count | integer | false | 10 | Number of returned devices. |
| order | string | false | + | Sort order (`+` or `-`). |
| sort | string | false | type | Sort field (for example `type`, `name`, `model`, `series`, `mac`, `network_name`, `serial_number`, `registered_by`, `created_time`, `modified_time`, `expired_date`, `license_status`, `ai_expired_date`). |
| search | string | false | - | Keyword search by common display fields. |

### Request Body

(EMPTY)

### Response Body Example

```json
{
  "size": 1,
  "devices": [
    {
      "id": "6108ff4f82bcdd7d877ad8a4",
      "hierarchy_view_id": "6100bfae95af6a16c69457c0",
      "network_id": "6100bfc495af6a16c69457c9",
      "network_name": "test_network",
      "name": "ECS1152FP-2",
      "type": "switch",
      "model": "ECS1152FP",
      "series": "Cloud",
      "mac": "db:4e:8d:e9:c1:76",
      "license_status": "active",
      "license_type": "pro",
      "serial_number": "2170G4F111D9",
      "registered_by": "user@example.com",
      "created_time": 1627979599000,
      "modified_time": 1627983288000,
      "registered_time": 1627979599000,
      "expired_date": 1720828800000
    }
  ]
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| size | integer | Returned device count. |
| devices | array[object] | Device list. |

### devices[] Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | Device id. |
| hierarchy_view_id | string | Hierarchy view id. |
| network_id | string | Network id. |
| network_name | string | Network name. |
| name | string | Device name. |
| type | string | Device type (`ap`, `switch`, `gateway`, `pdu`, `camera`, etc.). |
| model | string | Device model. |
| series | string | Device series. |
| mac | string | Device MAC. |
| license_status | string | License status. |
| license_type | string | License type. |
| serial_number | string | Device serial number. |
| registered_by | string | Registrar email. |
| created_time | integer | Creation timestamp in milliseconds. |
| modified_time | integer | Last modified timestamp in milliseconds. |
| registered_time | integer | Registration timestamp in milliseconds. |
| expired_date | integer | License expiration timestamp in milliseconds. |

### Usage Notes

- Use `devices[].id` for downstream APIs (`assign_license`, `patch_inventory`, `deregister_org_device`, `move_devices_between_orgs`, etc.).
- Never use MAC or serial as path `deviceId`.
