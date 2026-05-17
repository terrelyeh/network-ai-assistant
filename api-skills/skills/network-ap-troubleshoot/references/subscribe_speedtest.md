- description: Subscribe to real-time speedtest results

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| server | string | false | Speedtest server URL or "auto" (default: "auto") |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077"
}
```

### Internal Subscribe Format

```json
{
    "topic": "speedtest",
    "private": true,
    "options": {
        "server": "auto"
    }
}
```

### Response Body Example

```json
{
    "topic": "speedtest",
    "device": "88:dc:96:84:e1:67",
    "content": {
        "Download speed": "61.24 Mbps"
    }
}
```

Note: Content alternates between "Download speed" and "Upload speed" during the test. Results are realtime.
