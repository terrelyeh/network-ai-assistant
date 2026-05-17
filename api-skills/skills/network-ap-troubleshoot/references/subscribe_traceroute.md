- description: Subscribe to real-time traceroute results for a target host

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| host | string | true | Target host to traceroute (e.g., "www.google.com") |
| max_hop | integer | false | Maximum number of hops (default: 30) |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "host": "www.google.com",
    "max_hop": 30
}
```

### Internal Subscribe Format

```json
{
    "topic": "traceroute",
    "private": true,
    "options": {
        "host": "www.google.com",
        "max_hop": 30
    }
}
```

### Response Body Example

```json
{
    "topic": "traceroute",
    "device": "88:dc:96:84:e1:67",
    "content": {
        "hop": 1,
        "hop_list": [
            {
                "domain": "skc1-3022.hinet.net",
                "ip": "220.128.25.162",
                "latency": ["11.402 ms", "11.444 ms"]
            },
            {
                "domain": "aaaa.hinet.net",
                "ip": "220.128.25.13",
                "latency": ["10.222 ms"]
            }
        ]
    }
}
```
