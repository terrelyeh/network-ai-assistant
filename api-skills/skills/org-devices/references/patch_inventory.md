- method: PATCH
- path: /orgs/{orgId}/inventory/{deviceId}

Update device info or undo license association.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |
| deviceId | string | Device id from `get_inventory.devices[].id` only. |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "action": "patch_device_info",
  "name": "Device 01",
  "description": "new description"
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| action | string | true | `patch_device_info`, `undo_license`, or `undo_ai_license`. |
| name | string | false | New device name (`patch_device_info` only). |
| description | string | false | New description (`patch_device_info` only). |

### Action Notes

- `patch_device_info`: send `name` and/or `description`.
- `undo_license`: send only `{ "action": "undo_license" }`.
- `undo_ai_license`: send only `{ "action": "undo_ai_license" }`.

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

- `undo_license` and `undo_ai_license` are valid only during grace period; otherwise backend may return error.
- Never pass serial/MAC in path `deviceId`.
