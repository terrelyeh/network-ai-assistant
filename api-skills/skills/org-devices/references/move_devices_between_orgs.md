- method: POST
- path: /orgs/{orgId}/inventory/move

Move devices from source org to target org.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Source organization id (24-char hex). |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "org_id": "5d3a70dfae4a1400010a36d7",
  "device_ids": [
    "69115a2d479152e824e0d9af"
  ]
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| org_id | string | true | Target organization id (24-char hex). |
| device_ids | array[string] | true | Device ids from source org inventory (`get_inventory.devices[].id`). |

### Response Body Example

```json
{
  "code": 200,
  "message": "OK"
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| code | integer | Result code (`200` on success). |
| message | string | Result message. |

### Usage Notes

- Path `orgId` is source org; body `org_id` is target org.
- Moving a device also moves licenses associated with that device.
