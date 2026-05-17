Update an ACL block/white/VIP client's description or scope in network, AP's SSID profile, or Gateway.


### Request Body Example
> **Schema illustration only. Values are fictional. Do NOT use as PATCH body base.**
> Always use the actual GET response for the current network state.


#### Network
```json
{
  "description": "Client 1",
  "scope": "network",
  "access": "vip",
  "is_mld_client": false,
  "from_device_type": "ap",
  "to_device_type": "ap"
}
```

#### AP/SSID Profile
```json
{
  "description": "Client 2",
  "scope": "ssid",
  "access": "block",
  "ssid_profile_ids": ["5e5df1e1322204f7b0708ea8"],
  "is_mld_client": true,
  "from_device_type": "ap",
  "to_device_type": "ap"
}
```

#### Gateway
```json
{
  "description": "Client 3",
  "access": "white",
  "from_device_type": "gateway",
  "to_device_type": "gateway"
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| access | string | ✅ | Target ACL type. Enum: `block`, `white`, `vip`. |
| from_device_type | string | ✅ | Source device type of the ACL rule. Enum: `ap`, `gateway`. |
| to_device_type | string | ✅ | Destination device type of the ACL rule. Enum: `ap`, `gateway`. |
| description | string | - | Description (comment) of the ACL rule. |
| scope | string | - | Applies only when `device_type` is `ap`. Enum: `network`, `ssid`. |
| ssid_profile_ids | array[string] | - | Required (min 1 item) when `scope` is `ssid`. |
| is_mld_client | boolean | - | Set to `true` when `clientMac` refers to the MLD client's MAC address. Default: `false`. |
