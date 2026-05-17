- description: Subscribe to real-time WAN interface throughput (unit: B/s)

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| interface | string | false | WAN interface to monitor: `"WAN1"` (default), `"WAN2"`, `"WWAN"` |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "interface": "WAN1"
}
```

### Internal Subscribe Format

```json
[{"topic": "throughput", "options": {"interface": "WAN1"}}]
```

### Response Body Example

```json
{
    "topic": "throughput",
    "device": "88:dc:96:84:e1:67",
    "content": {
        "history": [
            {
                "Interface": "WAN1",
                "sent": 123,
                "rcvd": 456,
                "timestamp": "2024-01-01T00:00:00Z"
            }
        ]
    }
}
```
