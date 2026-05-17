- description: Subscribe to real-time switch device statistics

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
{
    "topic": "stat"
}
```

### Response Body Example

```json
{
    "topic": "stat",
    "content": {
        "cpu_load": 37,
        "memory_usage": {
            "used": 29,
            "cache_buffer": 6
        }
    }
}
```
