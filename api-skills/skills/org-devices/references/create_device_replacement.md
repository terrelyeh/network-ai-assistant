- method: POST
- path: /orgs/{orgId}/inventory/{deviceId}/replacement

Replace one device with another device in inventory.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |
| deviceId | string | Replaced (old) device id from inventory. |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "device_id": "6108fe9382bcdd7d877ad896",
  "mode": "replace"
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| device_id | string | true | Replacement (new) device id from inventory. |
| mode | string | true | `replace` or `replace_and_deregister`. |

### Mode Mapping

| Value | Meaning |
|---|---|
| replace | Replaced device is moved to inventory. |
| replace_and_deregister | Replaced device is de-registered for RMA flow. |

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

- Path `deviceId` and body `device_id` must be different device ids.
- Both ids must come from the same org `get_inventory` result and should be same model pair.
