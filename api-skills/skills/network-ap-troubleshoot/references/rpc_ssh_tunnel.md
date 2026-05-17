- description: Establish SSH tunnel to an AP device

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| ssh_ip | string | true | SSH server IP address |
| ssh_port | integer | true | SSH server port |
| ssh_session | string | true | SSH session identifier |
| user_email | string | true | Requesting user's email |
| user_role | string | true | Requesting user's role |
| user_session | string | true | User session identifier |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "ssh_ip": "192.168.1.100",
    "ssh_port": 22,
    "ssh_session": "sess-abc123",
    "user_email": "admin@example.com",
    "user_role": "admin",
    "user_session": "user-sess-xyz"
}
```

### Internal RPC Format

```json
{
    "method": "ssh_tunnel",
    "params": {
        "ssh": {
            "ip": "$ip",
            "port": "$port",
            "session": "$session"
        },
        "user": {
            "email": "$email",
            "role": "$role",
            "session": "$session"
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
