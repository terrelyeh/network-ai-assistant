- description: Subscribe to real-time speedtest results; supports server and source interface selection

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| server | string | false | Speedtest server URL or `"auto"` (default: `"auto"`) |
| interface | string | false | Source interface: `"default"` (default), `"WAN1"`, `"WAN2"`, `"WWAN"` |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077"
}
```

### Internal Subscribe Format

```json
[{"topic": "speedtest", "private": true, "options": {"server": "auto", "interface": "default"}}]
```

### Response Body Example

```json
{
    "topic": "speedtest",
    "device": "88:dc:96:84:e1:67",
    "content": {
        "history": [
            {
                "Download speed": "61.24 Mbps",
                "timestamp": "2024-01-01T00:00:01Z"
            },
            {
                "Upload speed": "20.10 Mbps",
                "timestamp": "2024-01-01T00:00:05Z"
            }
        ]
    }
}
```

Note: Content alternates between `"Download speed"` and `"Upload speed"` during the test. Results are real-time. Timeout is 90 seconds.
