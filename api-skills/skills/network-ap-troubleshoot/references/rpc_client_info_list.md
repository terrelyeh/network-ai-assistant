- description: Get detailed client info with optional SSID profile and band filter

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| ssid_profile_ids | array | false | List of SSID profile IDs to filter; omit or null for all SSIDs |
| band | string | false | Frequency band: "2_4g", "5g", "6g", or "all" (default: "all") |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "ssid_profile_ids": ["1234567890abcdef000000001", "1234567890abcdef000000002"],
    "band": "all"
}
```

### Internal RPC Format

```json
{
    "method": "client_info_list",
    "params": {
        "ssid_profile_id": ["1234567890abcdef000000001", "1234567890abcdef000000002"],
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
            "result": {
                "1234567890abcdef000000001": {
                    "2_4g": [{"mac": "00:aa:bb:cc:dd:10", "name": "abcd"}],
                    "5g": [
                        {"mac": "00:aa:bb:cc:dd:12", "name": "abcd"},
                        {"mac": "00:aa:bb:cc:dd:13", "name": "abcd"}
                    ],
                    "6g": [{"mac": "00:aa:bb:cc:dd:15", "name": "abcd"}]
                },
                "1234567890abcdef000000002": {
                    "2_4g": [{"mac": "00:aa:bb:cc:dd:13", "name": "abcd"}],
                    "5g": [{"mac": "00:aa:bb:cc:dd:13", "name": "abcd"}]
                }
            }
        }
    ]
}
```
