- description: Subscribe to real-time cable diagnostics for selected ports

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| ports | array[integer] | true | Target port numbers for cable diagnostics |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "ports": [1, 6, 7, 8]
}
```

### Internal Subscribe Format

```json
{
    "topic": "cable_diag",
    "options": {
        "ports": [1, 6, 7, 8]
    }
}
```

### Response Body Example

```json
{
    "topic": "cable_diag",
    "content": {
        "port": 1,
        "pair_a": {
            "status": "ok",
            "len": "10M"
        },
        "pair_b": {
            "status": "ok",
            "len": "10M"
        },
        "pair_c": {
            "status": "ok",
            "len": "10M"
        },
        "pair_d": {
            "status": "ok",
            "len": "10M"
        }
    }
}
```
