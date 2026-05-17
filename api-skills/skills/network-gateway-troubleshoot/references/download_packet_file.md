- description: Download a packet capture file from a specified WAN interface (PRO feature, gateway v1.2.45+)

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| interface | string | true | Capture interface: `"WAN1"`, `"WAN2"`, `"WWAN"` |
| duration | integer | false | Capture duration in seconds (default: `5`) |
| filter | string | false | BPF filter expression (default: `""`, no filter) |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "interface": "WAN1",
    "duration": 5
}
```

### Internal Download Payload (base64-encoded)

```json
{
    "file": "packet_file",
    "options": {
        "interface": "WAN1",
        "duration": 5
    }
}
```

### Response Body Example

```json
{
    "status_code": 200,
    "data": {
        "content": "<binary pcap content>"
    }
}
```

Note: PRO feature, requires gateway firmware v1.2.45 or later. Timeout is 60 seconds. The response content is a binary pcap file.
