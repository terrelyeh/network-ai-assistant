- description: Reset a PoE port on the gateway device

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| port_num | integer | true | PoE port number to reset (e.g. `1`, `2`) |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "port_num": 1
}
```

### Internal RPC Format

```json
{
    "method": "poe_reset",
    "params": {"port_num": 1}
}
```

### Response Body Example

```json
{
    "code": 200,
    "devices": [
        {
            "device": "00:90:7f:06:61:14",
            "code": 200,
            "result": {
                "status": "ok"
            }
        }
    ]
}
```
