- description: Download the ESG Root CA certificate from the gateway (gateway v1.2.85+)

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

### Internal Download Payload (base64-encoded)

```json
{
    "file": "ESG_Root_CA"
}
```

### Response Body Example

```json
{
    "status_code": 200,
    "data": {
        "content": "<PEM certificate content>"
    }
}
```

Note: Requires gateway firmware v1.2.85 or later. Timeout is 30 seconds.
