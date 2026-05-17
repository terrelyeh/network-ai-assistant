- description: Subscribe to real-time gateway port statistics (gateway v1.2.85+)

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
[{"topic": "port_stat"}]
```

### Response Body Example

```json
{
    "topic": "port_stat",
    "device": "88:dc:96:11:44:44",
    "content": {
        "time": 1626344101046,
        "ports": [
            {
                "id": "P1",
                "tx": 1245788,
                "rx": 56789,
                "link_speed": "1G",
                "crc": 0
            }
        ],
        "timestamp": "2024-01-01T00:00:00Z"
    }
}
```

Note: Requires gateway firmware v1.2.85 or later. When reporting results, include per-port link state, RX/TX counters, link speed, and highlight any ports with non-zero CRC errors or unexpected link state.
