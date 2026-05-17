- method: POST
- path: /orgs/{orgId}/inventory/{deviceId}/licenses

Associate a license to a specific device.

### Path Parameters

| Field | Type | Description |
|---|---|---|
| orgId | string | Target organization identifier (24-char hex). |
| deviceId | string | Device id from `get_inventory.devices[].id` (not MAC/serial). |

### Query Parameters

(EMPTY)

### Request Body Example

```json
{
  "days": 365,
  "license_type": "pro"
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| days | integer | true | License validity in days. |
| license_type | string | false | `pro`, `pro-r`, `pro-v`, `pro-lite`, `secupoint`, `unlimited`; omitted/null means default `pro`. |

### Response Body Example

```json
{
  "org_id": "6115e91491d5ef7f545ab984",
  "network_id": "6100bfc495af6a16c69457c9",
  "device_id": "6108ff4f82bcdd7d877ad8a4",
  "network_name": "test_network",
  "device_type": "ap",
  "model": "EWS377AP",
  "mac": "aa:bb:cc:dd:ee:ff",
  "serial_number": "2170G4F111D9",
  "registered_by": "user@example.com",
  "license_id": "615548211ac508f7e722510e",
  "license_status": "active",
  "license_type": "pro",
  "expired_date": 1720828800000
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| org_id | string | Organization id. |
| network_id | string | Network id. |
| device_id | string | Device id. |
| network_name | string | Network name. |
| device_type | string | Device type. |
| model | string | Device model. |
| mac | string | Device MAC. |
| serial_number | string | Device serial number. |
| registered_by | string | Device registrar. |
| license_id | string | Associated license id. |
| license_status | string | License status. |
| license_type | string | License type. |
| ai_license_status | string | AI license status when applicable. |
| ai_license_type | string | AI license type when applicable. |
| expired_date | integer | License expiration timestamp in milliseconds. |

### Usage Notes

- `deviceId` must come from `get_inventory.devices[].id`.
- Use this endpoint for one-device assignment flow (not bulk association).
