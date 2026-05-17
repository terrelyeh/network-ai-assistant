- description: Upgrade failsafe firmware on the AP device (3-digit version)

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| firmware_url | string | true | Failsafe firmware download URL |
| firmware_checksum | string | true | Failsafe firmware checksum |
| firmware_version | string | true | Failsafe firmware version (3 digits, e.g., "1.2.3") |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "firmware_url": "https://example.com/failsafe.bin",
    "firmware_checksum": "abc123",
    "firmware_version": "1.2.3"
}
```

### Internal RPC Format

```json
{
    "method": "failsafe_upgrade",
    "params": {
        "image": {
            "url": "$failsafe_fw_url",
            "checksum": "$failsafe_fw_checksum",
            "version": "$failsafe_fw_version"
        }
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
