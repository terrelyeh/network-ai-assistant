- description: Get available speedtest server list

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077"
}
```

### Internal RPC Format

```json
{"method": "speedtest_serverlist"}
```

### Response Body Example

```json
{
    "code": 200,
    "devices": [
        {
            "device": "00:90:7f:06:61:14",
            "code": 200,
            "result": {
                "ServersList": [
                    {
                        "Name": "Shulin District",
                        "URL": "http://gh-speedtest.bbtv.tw:8080/speedtest/upload.php",
                        "Country": "Taiwan",
                        "Sponsor": "Homeplus",
                        "Latitude": "24.981600",
                        "Longitude": "121.419900",
                        "Distance": "10.342609"
                    }
                ]
            }
        }
    ]
}
```

Note: Timeout is 5 seconds. Use the `URL` field from the chosen server as the `server` parameter for `subscribe_speedtest`.
