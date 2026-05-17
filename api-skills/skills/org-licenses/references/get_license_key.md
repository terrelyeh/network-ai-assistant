- method: GET
- path: /license-keys/{licenseKey}

Return metadata for a license key.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| licenseKey | string | License key string (for example `AAAAAA-BBBBBB-CCCCCC-DDDDDD`). |

### Query Parameters

(EMPTY)

### Request Body

(EMPTY)

### Response Body Example

```json
{
  "id": "615548211ac508f7e722510e",
  "license_key": "AAAAAA-BBBBBB-CCCCCC-DDDDDD",
  "license_category": "ap",
  "license_type": "pro",
  "status": "inactive",
  "units": 1,
  "duration": 365,
  "model": "AP-1YR-LIC",
  "issued_date": 1633050739928,
  "activated_date": null
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| id | string | License key record id. |
| license_key | string | License key string. |
| license_category | string | License category (`ap`, `switch`, `gateway`, `pdu`, `camera`, `ai`, etc.). |
| license_type | string | License type (`pro`, `pro-v`, `pro-r`, `pro-lite`, `connect`, `backup`, `ai`, etc.). |
| status | string | Key/license status. |
| units | integer | Number of license units in this key. |
| duration | integer | Validity days. |
| model | string | Model name. |
| issued_date | integer | Issued timestamp in milliseconds. |
| activated_date | integer \| null | Activated timestamp in milliseconds (when applicable). |
| engenius_ai_tokens | integer | AI tokens for AI-related licenses (`-999` may represent unlimited). |

### Usage Notes

- This endpoint is standalone (no `orgId` needed).
- Add flow should be: `get_license_key` -> show summary to user -> explicit confirmation -> `add_license_key`.
