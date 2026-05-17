- description: Upgrade firmware on the AP device (4-digit version)

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| firmware_url | string | true | Firmware download URL |
| firmware_checksum | string | true | Firmware checksum |
| firmware_version | string | true | Firmware version (4 digits, e.g., "1.2.3.4") |
| is_force | boolean | false | Force upgrade even if same version (default: true) |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "firmware_url": "https://example.com/firmware.bin",
    "firmware_checksum": "abc123",
    "firmware_version": "1.2.3.4",
    "is_force": true
}
```

### Internal RPC Format

```json
{
    "method": "upgrade",
    "params": {
        "image": {
            "url": "$firmware_url",
            "checksum": "$firmware_checksum",
            "version": "$firmware_version"
        },
        "is_force": true
    }
}
```

### Response Body Example

```json
{
    "code": 200,
    "devices": [
        {
            "device": "00:90:7f:06:61:14",
            "code": 200,
            "result": {
                "status": "ok"
            }
        }
    ]
}
```
