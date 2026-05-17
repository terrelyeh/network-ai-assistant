- description: Subscribe to real-time switch port statistics

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
    "topic": "port_stat"
}
```

### Response Body Example

```json
{
    "topic": "port_stat",
    "content": {
        "time": 1626344101046,
        "ports": [
            {
                "id": "1",
                "tx": 1245788,
                "rx": 56789,
                "link_speed": "1G",
                "crc": 0
            }
        ]
    }
}
```
