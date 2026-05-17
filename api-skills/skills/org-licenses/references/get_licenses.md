- method: GET
- path: /orgs/{orgId}/licenses

Return licenses under the target organization.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |

### Query Parameters

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| from | integer | false | 0 | Pagination start index. |
| count | integer | false | 10 | Number of items to return. |
| order | string | false | + | Sort order: `+` or `-`. |
| sort | string | false | activated_date | Sort field (`license_type`, `license_key`, `duration`, `issued_date`, `activated_date`, `time_remaining`, `status`, `associated_device`, `license_key_model`, `added_by`). |
| license_category | string | false | - | `ap`, `switch`, `gateway`, `pdu`, `switch_extender`, `epc`, `camera`, `ai`. |
| license_type | string | false | - | Includes `pro_license` for per-device listing. |
| is_co_terminated | boolean | false | - | Filter Co-Term licenses. |
| is_epc_device_only | boolean | false | - | Filter EPC device-only licenses. |
| status | string | false | - | `inactive`, `active`, `merging`, `merged`, `expired`, `canceled`. |

### Request Body

(EMPTY)

### Response Body Example

```json
{
  "size": 2,
  "licenses": [
    {
      "id": "615548211ac508f7e722510e",
      "license_key": "AAAAAA-BBBBBB-CCCCCC-DDDDDD",
      "license_key_model": "AP-1YR-LIC",
      "license_type": "pro",
      "license_category": "ap",
      "status": "active",
      "device_id": "6108ff4f82bcdd7d877ad8a4",
      "device_name": "My-AP",
      "added_by": "user@example.com",
      "duration": 365,
      "time_remaining": 250,
      "issued_date": 1633050739928,
      "activated_date": 1640999539000,
      "associated_date": 1640999539000
    }
  ],
  "available_ai_tokens": null
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| size | integer | Returned license item count. |
| licenses | array[object] | License list. |
| available_ai_tokens | integer \| null | AI token balance when applicable. |

### licenses[] Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | License id. |
| license_key | string | License key. |
| license_key_model | string | License key model name. |
| license_type | string | License type (`pro`, `pro-v`, `pro-r`, `pro-lite`, `connect`, `backup`, `ai`, etc.). |
| license_category | string | Device category (`ap`, `switch`, `gateway`, `pdu`, `camera`, etc.). |
| status | string | `inactive`, `active`, `merging`, `merged`, `expired`, `canceled`. |
| device_id | string | Associated device id when associated. |
| device_name | string | Associated device name. |
| added_by | string | User who added this license. |
| duration | integer | Validity days. |
| time_remaining | integer | Remaining days. |
| issued_date | integer | Issued timestamp in milliseconds. |
| activated_date | integer | Activated timestamp in milliseconds. |
| associated_date | integer | Association timestamp in milliseconds. |

### Usage Notes

- Use `license_type=pro_license` when user asks for Per-Device licenses.
- `associated_licenses` and move/assign flows must use `licenses[].id`, never `license_key`.
