- description: Scan WiFi channels on all bands or a specific band

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
    "band": "2_4g"
}
```

### Internal RPC Format

```json
{
    "method": "wifi_scan",
    "params": {
        "band": "2_4g"
    },
    "timeout": 60
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
                    "bssids": ["00:90:7f:06:61:15", "06:90:7f:06:61:15"],
                    "sta_count": 2,
                    "ap_stat": [
                        {
                            "power": -71,
                            "chwidth": "HT20",
                            "chan": 6,
                            "mode": "AC",
                            "ssid": "abc",
                            "bssid": "aa:75:dc:a0:ff:ff"
                        }
                    ]
                }
            ]
        }
    ]
}
```

Note: Timeout is 60 seconds.
