- description: Download an ESG EAP client certificate for a specific user email (gateway v1.2.100+)

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| user_email | string | true | Email address of the certificate owner |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "user_email": "user@example.com"
}
```

### Internal Download Payload (base64-encoded)

```json
{
    "file": "esg_eap_cert",
    "options": {
        "user_email": "user@example.com"
    }
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

Note: Requires gateway firmware v1.2.100 or later. Timeout is 30 seconds.
