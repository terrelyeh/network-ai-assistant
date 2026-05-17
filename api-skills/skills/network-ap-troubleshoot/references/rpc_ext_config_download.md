- description: Download external config file to the AP (e.g., URL filtering config or Lionic signature)

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| name | string | true | Config name: "url_filtering_config" or "lionic_signature" |
| url | string | true | Config file download URL |
| checksum | string | true | Config file checksum |
| version | string | true | Config file version |
| file_type | string | false | File type (required for "lionic_signature") |

### Request Body Example (url_filtering_config)

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "name": "url_filtering_config",
    "url": "https://example.com/url_filter.conf",
    "checksum": "abc123",
    "version": "1.0.0"
}
```

### Request Body Example (lionic_signature)

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "name": "lionic_signature",
    "file_type": "$lionic_sig_type",
    "url": "https://example.com/lionic_sig.bin",
    "checksum": "abc123",
    "version": "2.0.0"
}
```

### Internal RPC Format (url_filtering_config)

```json
{
    "method": "ext_config_download",
    "params": {
        "name": "url_filtering_config",
        "file": {
            "url": "$ext_config_url",
            "checksum": "$ext_config_checksum",
            "version": "$ext_config_version"
        }
    }
}
```

### Internal RPC Format (lionic_signature)

```json
{
    "method": "ext_config_download",
    "params": {
        "name": "lionic_signature",
        "file": {
            "type": "$lionic_sig_type",
            "url": "$ext_config_url",
            "checksum": "$ext_config_checksum",
            "version": "$ext_config_version"
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
