- description: Subscribe to real-time traceroute results; supports interface and IP version (v4/v6) selection

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| host | string | true | Target host to traceroute (IP or domain) |
| max_hop | integer | false | Maximum number of hops (default: `30`) |
| interface | string | false | Source interface: `"WAN1"` (default), `"WAN2"`, `"WWAN"`, `"default"` |
| ip_version | string | false | IP version: `"v4"` (default) or `"v6"` (requires gateway v1.2.80+) |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "host": "8.8.8.8"
}
```

### Internal Subscribe Format

```json
[{"topic": "traceroute", "private": true, "options": {"host": "8.8.8.8", "max_hop": 30, "interface": "WAN1", "type": "v4"}}]
```

### Response Body Example

```json
{
    "topic": "traceroute",
    "device": "88:dc:96:84:e1:67",
    "content": {
        "hop": 3,
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
        ],
        "timestamp": "2024-01-01T00:00:00Z"
    }
}
```

Note: Timeout is 60 seconds.
