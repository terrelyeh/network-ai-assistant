- description: Download a real-time firewall log file filtered by rule type (gateway v1.2.50+)

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| filter | string | false | Firewall rule type filter: `"0"` = outbound (default), `"1"` = port forwarding, `"2"` = 1:1 NAT |
| duration | integer | false | Collection duration in seconds (default: `5`) |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "filter": "0",
    "duration": 5
}
```

### Internal Download Payload (base64-encoded)

```json
{
    "file": "realtime_firewalllog_file",
    "options": {
        "filter": "0",
        "duration": 5
    }
}
```

### Response Body Example

```json
{
    "status_code": 200,
    "data": {
        "content": "<firewall log text content>"
    }
}
```

Note: Requires gateway firmware v1.2.50 or later. Timeout is 30 seconds.
