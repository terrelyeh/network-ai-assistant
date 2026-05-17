- description: Subscribe to real-time spectrum scan data for a specific band (not supported on Dakota platform)

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
    "topic": "spectrum_scan",
    "options": {
        "band": "5g"
    }
}
```

### Band-specific Parameters

| Band | Channels | ht_mode | num_fft_bins |
|---|---|---|---|
| 2.4G | 3, 8, 13 | ht40 | 32 |
| 5G (general) | 36, 52, 100, 116, 149 | ht80 | 64 |
| 5G chan 132 | 132 | ht40 | 32 |
| 5G chan 140, 165 | 140, 165 | ht20 | 16 |

### Response Body Example

```json
{
    "topic": "spectrum_scan",
    "device": "88:dc:96:84:e1:67",
    "content": {
        "spectrum_scan": [
            {
                "band": "2_4g",
                "scan_count": 2,
                "num_samples": 100,
                "num_fft_bins": 32,
                "ht_mode": "ht40",
                "results": [
                    {
                        "chan": 3,
                        "center_frequency": 2422,
                        "result": ["110,...,-109"]
                    }
                ]
            }
        ]
    }
}
```
