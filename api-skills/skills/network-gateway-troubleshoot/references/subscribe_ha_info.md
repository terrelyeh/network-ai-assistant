- description: Subscribe to real-time HA (High Availability) status (gateway v1.2.85+)

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
[{"topic": "ha_info"}]
```

### Response Body Example

```json
{
    "topic": "ha_info",
    "device": "88:dc:96:11:44:44",
    "content": {
        "time": 1626344101046,
        "ha": {
            "sync_port_status": 0,
            "active_status": 0,
            "ha_port": 0,
            "firmware_version_check": 0,
            "sync_port_ip_overlapped": 0,
            "error_occurred": []
        },
        "timestamp": "2024-01-01T00:00:00Z"
    }
}
```

Note: Requires gateway firmware v1.2.85 or later. `active_status: 0` means the device is in active role. `error_occurred` lists active HA fault conditions (e.g. `"sync_prot_link_down"`).
