- method: POST
- path: /orgs/{orgId}/license-keys/{licenseKey}/auto-association

Auto-associate a license key's units to selected devices.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |
| licenseKey | string | License key already added to this org. |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "device_ids": [
    "6108fe9382bcdd7d877ad896",
    "6108fe9382bcdd7d877ad897"
  ]
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| device_ids | array[string] | true | Device ids from `get_inventory.devices[].id` only. |

### Response Body Example

```json
{
  "code": 200,
  "message": "OK",
  "license_key": "AAAAAA-BBBBBB-CCCCCC-DDDDDD",
  "licenses": [
    {
      "id": "615548211ac508f7e722510e",
      "status": "active",
      "mac": "aa:bb:cc:dd:ee:ff"
    }
  ]
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| code | integer | Result code (`200` on success). |
| message | string | Result message. |
| license_key | string | Target license key. |
| licenses | array[object] | Per-unit association results. |

### Usage Notes

- `device_ids` must be device object ids (24-char hex), never MAC/serial.
- If provided devices are fewer than key units, remaining units stay unassociated.
