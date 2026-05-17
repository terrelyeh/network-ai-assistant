- description: Subscribe to real-time ARP table entries

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| page_size | integer | true | Max entries per page |
| ip | string | false | Optional filter by IP address (e.g. `"192.168.1.1"`) |
| vid | integer | false | Optional filter by VLAN id |
| mac | string | false | Optional filter by MAC address |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "page_size": 100,
    "ip": "192.168.1.254",
    "vid": 12,
    "mac": "00:11:22:33:44:55"
}
```

### Internal Subscribe Format

```json
{
    "topic": "arp_list",
    "options": {
        "page_size": 100,
        "ip": "192.168.1.254",
        "vid": 12,
        "mac": "00:11:22:33:44:55"
    }
}
```

### Response Body Example

```json
{
    "topic": "arp_list",
    "content": {
        "total_entries": 1000,
        "entries": "192.168.1.1,001122334455,1;192.168.1.254,001122334456,1"
    }
}
```
