- description: Subscribe to real-time ping results for a target host; supports source interface selection

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| host | string | true | Target host to ping (IP or domain, e.g. `"8.8.8.8"` or `"www.google.com"`) |
| interface | string | false | Source interface: `"default"` (default), `"WAN1"`, `"WAN2"`, `"WWAN"`, or LAN ID |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "host": "8.8.8.8"
}
```

### Internal Subscribe Format

```json
[{"topic": "ping", "options": {"host": "8.8.8.8", "interface": "default"}}]
```

### Response Body Example

```json
{
    "topic": "ping",
    "device": "88:dc:96:84:e1:67",
    "content": {
        "history": [
            {
                "time": "2.18 ms",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        ]
    }
}
```
