- description: Get channel utilization for all channels on a specific band or all bands

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| band | string | false | Frequency band: "2_4g", "5g", "6g", or "all" (default: "all") |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "band": "all"
}
```

### Internal RPC Format

```json
{
    "method": "all_chan_util",
    "params": {
        "band": "all"
    },
    "timeout": 30
}
```

### Response Body Example

```json
{
    "code": 200,
    "devices": [
        {
            "device": "88:dc:96:84:e1:67",
            "code": 200,
            "result": [
                {
                    "band": "2_4g",
                    "ht_mode": "HT20",
                    "all_chan_list": [
                        {"channel": 1, "chan_util": 15, "non_wifi_util": 15},
                        {"channel": 13, "chan_util": 3, "non_wifi_util": 15}
                    ]
                }
            ]
        }
    ]
}
```

Note: Timeout is 50 seconds.
