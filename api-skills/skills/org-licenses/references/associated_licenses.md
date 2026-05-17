- method: POST
- path: /orgs/{orgId}/licenses/association

Bind existing license ids to device ids.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Source organization id (24-char hex). |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "license_ids": [
    "69b7c4427621a6c1995f9a90"
  ],
  "device_ids": [
    "6942689eb33068658ca248a0"
  ]
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| license_ids | array[string] | true | License ids from `get_licenses.licenses[].id` only. |
| device_ids | array[string] | true | Device ids from `get_inventory.devices[].id` only. |

### Response Body Example

```json
{
  "associated_licenses": [
    {
      "id": "69b7c4427621a6c1995f9a90",
      "license_key": "69B7C4-336CB3-0903EC-01A55D",
      "status": "active",
      "device_id": "6942689eb33068658ca248a0",
      "mac": "aa:bb:cc:dd:ee:ff"
    }
  ]
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| associated_licenses | array[object] | Associated license results. |

### Usage Notes

- Request accepts only ObjectId values; never pass `license_key`, MAC, or serial.
- Recommended flow: `get_licenses` -> pick eligible `licenses[].id` -> `get_inventory` -> pick `devices[].id` -> call this API.
