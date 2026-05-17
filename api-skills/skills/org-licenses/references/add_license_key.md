- method: POST
- path: /orgs/{orgId}/license-keys/{licenseKey}

Add a license key into an organization.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |
| licenseKey | string | License key string to add. |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "added_by": "user@example.com"
}
```

### Request Body Schema

Optional object.

| Field | Type | Required | Description |
|---|---|---|---|
| added_by | string | false | Optional operator email if backend supports recording it. |

### Response Body Example

```json
{
  "code": 200,
  "message": "OK",
  "license_key": "AAAAAA-BBBBBB-CCCCCC-DDDDDD",
  "license_category": "ap",
  "license_type": "pro",
  "units": 1,
  "duration": 365
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| code | integer | Result code (`200` on success). |
| message | string | Result message. |
| license_key | string | Added license key string. |
| license_category | string | License category. |
| license_type | string | License type. |
| units | integer | Units added to org by this key. |
| duration | integer | License duration in days. |
| licenses | array[object] | Expanded license units (when backend returns details). |

### Usage Notes

- Mandatory sequence: `get_license_key` -> show key summary -> explicit user confirmation -> call this API.
- Never call this endpoint directly without preview/confirmation step.
