- description: Subscribe to real-time client forwarding database entries

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| page_size | integer | true | Max entries per page |
| port | string | false | Optional filter by port id (physical: `"1"` to `"52"`, trunk: `"t1"` to `"t8"`) |
| vid | integer | false | Optional filter by VLAN id |
| mac | string | false | Optional filter by MAC address |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "page_size": 100,
    "port": "1",
    "vid": 12,
    "mac": "00:11:22:33:44:55"
}
```

### Internal Subscribe Format

```json
{
    "topic": "fdb_list",
    "options": {
        "page_size": 100,
        "port": "1",
        "vid": 12,
        "mac": "00:11:22:33:44:55"
    }
}
```

### Response Body Example

```json
{
    "topic": "fdb_list",
    "content": {
        "total_entries": 8000,
        "entries": "1,001122334455,1;1,001234567890,1"
    }
}
```
