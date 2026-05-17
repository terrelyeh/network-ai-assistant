- description: Subscribe to real-time traceroute results for a target host

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| host | string | true | Target host to traceroute (IP or domain) |

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
    "topic": "traceroute",
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
    "content": {
        "hop": 1,
        "hop_list": [
            {
                "domain": "skc1-3022.hinet.net",
                "ip": "220.128.25.162",
                "latency": [
                    "11.402 ms",
                    "11.444 ms"
                ]
            },
            {
                "domain": "aaaa.hinet.net",
                "ip": "220.128.25.13",
                "latency": [
                    "10.222 ms"
                ]
            }
        ]
    }
}
```
