- description: Subscribe to all channel utilization data for a specific band

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
    "topic": "all_channel_utilization",
    "options": {
        "band": "5g"
    }
}
```

### Response Body Example

```json
{
    "topic": "all_channel_utilization",
    "device": "88:dc:96:84:e1:67",
    "content": [
        {
            "band": "2_4g",
            "ht_mode": "HT20",
            "all_chan_util": [
                {"channel": 1, "chan_util": 15, "non_wifi_util": 15},
                {"channel": 2, "chan_util": 80, "non_wifi_util": 12}
            ]
        },
        {
            "band": "2_4g",
            "ht_mode": "HT40",
            "all_chan_util": [
                {"channel": 1, "chan_util": 15, "non_wifi_util": 15},
                {"channel": 2, "chan_util": 80, "non_wifi_util": 12}
            ]
        }
    ]
}
```

Note: Updates once per second.
