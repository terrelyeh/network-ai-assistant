- description: Subscribe to real-time ping results for a target host

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| host | string | true | Target host to ping (IP or domain) |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "host": "8.8.8.8"
}
```

### Internal Subscribe Format

```json
{
    "topic": "ping",
    "options": {
        "host": "www.google.com"
    }
}
```

### Response Body Example

```json
{
    "topic": "ping",
    "device": "88:dc:96:84:e1:67",
    "content": {
        "time": "2.18 ms"
    }
}
```
