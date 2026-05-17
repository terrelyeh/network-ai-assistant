- description: Subscribe to real-time VPN peer status (PRO feature)

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077"
}
```

### Internal Subscribe Format

```json
[{"topic": "vpnpeer_status"}]
```

### Response Body Example

```json
{
    "topic": "vpnpeer_status",
    "device": "88:dc:96:11:44:44",
    "content": {
        "vpnpeer_status": [
            {
                "is_engenius": 1,
                "latency": 0,
                "network_name": "6361dee5ea7d87533219be6e",
                "public_wan_ip": "1.163.44.189",
                "sent": 0,
                "rcvd": 0,
                "status": 0,
                "uptime": 0
            }
        ],
        "timestamp": "2024-01-01T00:00:00Z"
    }
}
```

Note: This is a PRO feature. `status: 0` means connected, non-zero means disconnected.
