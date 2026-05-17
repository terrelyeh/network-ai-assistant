- description: Download external config file to the gateway (e.g., URL filtering config or Lionic signature)

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| name | string | true | Config name (e.g. `"url_filtering_config"`) |
| url | string | true | Config file download URL |
| checksum | string | true | Config file checksum |
| version | string | true | Config file version |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "name": "url_filtering_config",
    "url": "https://example.com/config.bin",
    "checksum": "abc123",
    "version": "1.0.0"
}
```

### Internal RPC Format

```json
{
    "method": "ext_config_download",
    "params": {
        "name": "url_filtering_config",
        "file": {
            "url": "https://example.com/config.bin",
            "checksum": "abc123",
            "version": "1.0.0"
        }
    }
}
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
                "status": "ok"
            }
        }
    ]
}
```
