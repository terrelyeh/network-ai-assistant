Return hierarchy views and networks of the organization.

### Response Body Type

- `array[object]`

### Hierarchy View Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | Hierarchy view identifier. For root node, this is the root HV id. |
| name | string | Hierarchy view name. |
| org_id | string | Organization identifier (usually appears on root HV item). |
| parent_hierarchy_view_id | string | Parent HV id. Exists on non-root hierarchy view items. |
| hierarchy_views | array[string] | Child hierarchy view ids under this node. |
| networks | array[object] | Networks directly under this hierarchy view. |
| created_time | integer | Creation timestamp in milliseconds. |
| modified_time | integer | Last update timestamp in milliseconds. |

### networks[] Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | Network identifier. |
| name | string | Network name. |
| parent_hierarchy_view_id | string | The HV id this network belongs to (use as `hierarchy_view_id` in memberships patch). |
| description | string | Network description text. |
| country | string | Country setting of the network. |
| time_zone | string | Time zone setting in IANA format. |
| local_credential | string | Local credential mode (`default`, `empty`, `customized`). |
| device_counts | integer | Total device count in this network. |
| client_counts | integer | Total client count in this network. |
| ap_counts | integer | AP device count. |
| switch_counts | integer | Switch device count. |
| gateway_counts | integer | Gateway device count. |
| pdu_counts | integer | PDU device count. |
| nvs_counts | integer | NVS device count. |
| camera_counts | integer | Camera device count. |
| switch_extender_counts | integer | Switch extender device count. |
| skykey_counts | integer | SkyKey device count. |
| bsc_counts | integer | BSC device count. |
| users | array[object] | Network member list. |
| created_time | integer | Creation timestamp in milliseconds. |
| modified_time | integer | Last update timestamp in milliseconds. |

### networks[].users[] Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | User identifier. |
| email | string | User email. |
| family_name | string | User family/last name. |
| given_name | string | User given/first name. |
| role | string | User role in the network (`admin`, `viewer`, etc.). |
| created_time | integer | Membership creation timestamp in milliseconds. |
| modified_time | integer | Membership update timestamp in milliseconds. |

### Usage Notes

1. `root_hv_id` should be parsed from the HV item that contains `org_id`.
2. `hv_id` should be parsed from non-root HV items (those with `parent_hierarchy_view_id`).
3. For network permission patch, use:
   - `network_id` = `networks[].id`
   - `hierarchy_view_id` = `networks[].parent_hierarchy_view_id`

### Response Body Example

```json
[
  {
    "id": "5c1deea9c48a27ea74e0a020",
    "name": "Root HV",
    "org_id": "5c1deea9c48a27ea74e0a03c",
    "hierarchy_views": [
      "5c1deea9c48a27ea74e0a024"
    ],
    "networks": [
      {
        "id": "5b574c4b776fb10001bc66e7",
        "name": "Network 01",
        "client_counts": 10,
        "ap_counts": 5,
        "switch_counts": 1,
        "gateway_counts": 1,
        "pdu_counts": 1,
        "nvs_counts": 2,
        "camera_counts": 1,
        "switch_extender_counts": 1,
        "skykey_counts": 0,
        "bsc_counts": 0,
        "parent_hierarchy_view_id": "5c1deea9c48a27ea74e0a020",
        "description": "Network 01 description",
        "device_counts": 12,
        "country": "USA",
        "time_zone": "America/Los_Angeles",
        "local_credential": "default",
        "users": [
          {
            "id": "453f19a6920d53618e57b729",
            "email": "admin@senao.com",
            "family_name": "senao",
            "given_name": "cloud",
            "role": "admin",
            "created_time": 1530092619000,
            "modified_time": 1530092619000
          }
        ],
        "created_time": 1530092619000,
        "modified_time": 1530092619000
      }
    ],
    "created_time": 1530091921000,
    "modified_time": 1530091921000
  }
]
```
