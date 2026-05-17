- method: DELETE
- path: /orgs/{orgId}/devices

Remove one or more devices from networks.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |

### Query Parameters

(EMPTY)

### Request Body Example

```json
[
  {
    "device_id": "59d72645g799c000126e388",
    "network_id": "59d72645g799c000126e389"
  }
]
```

### Request Body Item Schema

| Field | Type | Required | Description |
|---|---|---|---|
| device_id | string | true | Device id to remove from network. |
| network_id | string | true | Network id where the device is currently assigned. |

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

- For de-register flow, remove from network with this API first, then call `deregister_org_device`.
