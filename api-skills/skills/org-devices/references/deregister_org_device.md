- method: DELETE
- path: /orgs/{orgId}/inventory/{deviceId}

De-register a device from organization inventory.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |
| deviceId | string | Device id from `get_inventory.devices[].id`. |

### Query Parameters

(EMPTY)

### Request Body

(EMPTY)

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

- If device is still assigned to a network (`network_id` exists), call `delete_devices` first.
- For multiple devices, call this API once per device id.
