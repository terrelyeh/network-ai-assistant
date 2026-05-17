- description: Subscribe to real-time channel utilization for a specific band

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| band | string | true | Frequency band: "2_4g", "5g", or "6g" |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "band": "5g"
}
```

### Internal Subscribe Format

```json
{
    "topic": "channel_utilization",
    "options": {
        "band": "5g"
    }
}
```

### Response Body Example

```json
{
    "topic": "channel_utilization",
    "device": "88:dc:96:84:e1:67",
    "content": {
        "channel": 13,
        "chan_util": 97,
        "non_wifi_util": 20
    }
}
```

Note: Updates once per second.
