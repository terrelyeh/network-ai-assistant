- description: Send Radius Change of Authorization (COA) or Disconnect request to kick clients by username or MAC

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| code | integer | true | COA code: 40 (Disconnect-Request) or 43 (CoA-Request) |
| avps | array | true | Radius Attribute Value Pairs |
| ssid_profile_ids | array | false | SSID profile IDs to scope the operation; omit for all SSIDs |
| timeout | integer | false | Timeout in seconds (default: 30) |

#### avps item schema

| Field | Type | Required | Description |
|---|---|---|---|
| User-Name | string | false | Client login username |
| Called-Station-Id | array | false | List of client MAC addresses |

#### User-Name / Called-Station-Id combinations

| User-Name | Called-Station-Id | Effect |
|---|---|---|
| provided | not provided | Disconnect and logout all clients with this username |
| not provided | provided | Disconnect these client MACs |
| provided | provided | Disconnect these client MACs only if using this username |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "code": 40,
    "ssid_profile_ids": ["ssid_profile_id1", "ssid_profile_id2"],
    "avps": [
        {
            "User-Name": "username1",
            "Called-Station-Id": ["mac1", "mac2"]
        }
    ],
    "timeout": 30
}
```

### Internal RPC Format

```json
{
    "method": "radius_coa",
    "params": {
        "code": 40,
        "ssid_profile_id": ["ssid_profile_id1", "ssid_profile_id2"],
        "AVPs": [
            {
                "User-Name": "username1",
                "Called-Station-Id": ["mac1", "mac2"]
            }
        ],
        "timeout": 30
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
                "ssid_profile_id1": ["mac1", "mac2"],
                "ssid_profile_id2": [],
                "ssid_profile_id3": ["mac3"]
            }
        }
    ]
}
```

Note: Result lists the disconnected MAC addresses per SSID profile ID.
