- description: Upload a file (e.g., WIDS record) from AP to a pre-signed URL

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| file_type | string | true | Type of file (e.g., "wids_record") |
| file_id | string | true | File record identifier |
| url | string | true | Pre-signed S3 URL to upload to |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "file_type": "wids_record",
    "file_id": "RF-88DC96CCDD10-2-17c791d249c-1a",
    "url": "https://ezmcloud-v2-dev-kdumps.s3.amazonaws.com/wids/XXXXXXX"
}
```

### Internal RPC Format

```json
{
    "method": "file_upload",
    "params": {
        "type": "wids_record",
        "id": "RF-88DC96CCDD10-2-17c791d249c-1a",
        "url": "https://ezmcloud-v2-dev-kdumps.s3.amazonaws.com/wids/XXXXXXX"
    }
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
                "size": 111234124,
                "checksum": "a99acc80c3da9a5b2150f703b7a0c8f673ea2935eace9b1fde89a8913966bcc4"
            }
        }
    ]
}
```
