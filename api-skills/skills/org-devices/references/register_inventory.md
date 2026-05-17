- method: POST
- path: /orgs/{orgId}/inventory

Register device serial numbers into organization inventory.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |

### Query Parameters

(EMPTY)

### Request Body Example

```json
[
  { "serial_number": "1650QCHPJ6C2" },
  { "serial_number": "17A1QCH326M1" }
]
```

### Request Body Item Schema

| Field | Type | Required | Description |
|---|---|---|---|
| serial_number | string | true | Device serial number to register. |

### Response Body Example

```json
[
  {
    "code": 200,
    "message": "OK",
    "status": "ok",
    "device_id": "59d72645g799c000126e38e",
    "serial_number": "1650QCHPJ6C2",
    "type": "ap",
    "mac": "dd:5f:f6:31:7a:bb",
    "model": "EWS360AP",
    "series": "Cloud",
    "license_status": "active",
    "registered_by": "user@example.com",
    "created_time": 1521535457869
  },
  {
    "code": 404,
    "message": "Not Found",
    "status": "unexisting",
    "serial_number": "17A1QCH326M1"
  }
]
```

### Response Body Item Schema

| Field | Type | Description |
|---|---|---|
| code | integer | Per-item result code. |
| message | string | Per-item message. |
| status | string | `ok`, `invalid`, `unexisting`, `used`, `error`. |
| serial_number | string | Input serial number. |
| device_id | string | Returned when registration succeeds. |
| type | string | Device type when successful. |
| mac | string | Device MAC when successful. |
| model | string | Device model when successful. |
| series | string | Device series when successful. |
| license_status | string | License status when successful. |

### Usage Notes

- Response is index-aligned with request array; inspect each item status instead of assuming all success.
