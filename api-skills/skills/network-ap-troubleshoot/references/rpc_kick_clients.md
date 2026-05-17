- description: Disconnect specified clients from the AP

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| clients | array | true | List of objects with ssid_id and mac |

#### clients item schema

| Field | Type | Required | Description |
|---|---|---|---|
| ssid_id | string | true | SSID profile ID |
| mac | string | true | Client MAC address (with colons) |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "clients": [
        {
            "ssid_id": "68ff2d8d5c048e7e2f7d3001",
            "mac": "00:11:22:33:44:55"
        },
        {
            "ssid_id": "68ff2d8d5c048e7e2f7d3001",
            "mac": "00:11:22:33:44:66"
        }
    ]
}
```

### Internal RPC Format

```json
{
    "method": "kick_clients",
    "params": {
        "ssids": [
            {"ssid_id": "$ssidid", "mac": "$MAC_with_colon"}
        ]
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
