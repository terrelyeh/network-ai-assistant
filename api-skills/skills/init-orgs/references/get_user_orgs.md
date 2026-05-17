- method: GET
- path: /user/orgs

Return organizations available to the authenticated user.

### Path Parameters

(EMPTY)

### Query Parameters

(EMPTY)

### Request Body

(EMPTY)

### Response Body Example

```json
[
  {
    "id": "6115e91491d5ef7f545ab984",
    "name": "Org_Reducing_Test",
    "creator": "603f3131feb45fcae6135ab5",
    "description": "test",
    "country": "Spain",
    "time_zone": "Europe/Madrid",
    "is_tfa_enable": false,
    "ap_license_mode": "pro",
    "switch_license_mode": "pro",
    "gateway_license_mode": "pro",
    "pdu_license_mode": "pro",
    "expired_devices_count": 3,
    "expired_devices_count_in_30_days": 0,
    "network_count": 14,
    "inventory_count": 29,
    "managed_count": 16,
    "users": [
      {
        "id": "63a2a6b7bff67708c9c6725b",
        "email": "senao@senao.com",
        "role": "admin",
        "created_time": 1709541621000,
        "modified_time": 1709541621000
      }
    ],
    "created_time": 1628825876000,
    "modified_time": 1707967326000
  }
]
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| id | string | Organization id (use as downstream `orgId`). |
| name | string | Organization display name. |
| creator | string | Organization creator user id. |
| description | string | Organization description. |
| country | string | Country setting. |
| time_zone | string | IANA time zone. |
| is_tfa_enable | boolean | Whether org 2FA is enabled. |
| ap_license_mode | string | AP license mode (`basic` or `pro`). |
| switch_license_mode | string | Switch license mode (`basic` or `pro`). |
| gateway_license_mode | string | Gateway license mode (`basic` or `pro`). |
| pdu_license_mode | string | PDU license mode (`basic` or `pro`). |
| expired_devices_count | integer | Already expired devices count. |
| expired_devices_count_in_30_days | integer | Devices expiring within 30 days. |
| network_count | integer | Total network count. |
| inventory_count | integer | Total inventory count. |
| managed_count | integer | Total managed device count. |
| users | array[object] | Org user memberships. |
| created_time | integer | Creation timestamp in milliseconds. |
| modified_time | integer | Last modified timestamp in milliseconds. |

### users[] Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | User id. |
| email | string | User email. |
| role | string | Org role (`admin` or `viewer`). |
| created_time | integer | Membership creation timestamp in milliseconds. |
| modified_time | integer | Membership update timestamp in milliseconds. |

### Usage Notes

- Always resolve `orgId` from this API before calling org-scoped endpoints.
- When user gives org name, match by `name` first, then use matched `id`.
