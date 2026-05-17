- description: Subscribe to real-time throughput data for a specific band (unit: B/s)

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
    "topic": "throughput",
    "options": {
        "band": "5g"
    }
}
```

### Response Body Example

```json
{
    "topic": "throughput",
    "device": "88:dc:96:84:e1:67",
    "content": {
        "download": 0,
        "upload": 194
    }
}
```

Note: Updates once per second. Unit is B/s.
