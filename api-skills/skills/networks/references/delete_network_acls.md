Remove clients from the ACL blocklist, allowlist, or VIP client list in bulk.

### Request Body Example


```json
{
  "access": "block",
  "clients": [
    { "scope": "network", "mac": "aa:bb:cc:dd:ee:f1", "is_mld_client": false, "device_type": "ap" },
    { "scope": "ssid",    "mac": "1a:bb:cc:dd:ee:f2", "is_mld_client": false, "device_type": "ap" },
    { "scope": "ssid",    "mac": "2a:bb:cc:dd:ee:f3", "is_mld_client": true,  "device_type": "ap" },
    { "mac": "3a:bb:cc:dd:ee:f1", "device_type": "gateway" }
  ]
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| access | string | ✅ | ACL type to delete from. Enum: `block`, `white`, `vip`. |
| clients | array[object] | ✅ | List of clients to remove. |

### clients[] Item Schema

| Field | Type | Required | Description |
|---|---|---|---|
| mac | string | ✅ | Client MAC address. When `is_mld_client` is `true` for AP, this is the `mld_mac_addr`. |
| device_type | string | ✅ | Device type of the ACL rule. Enum: `ap`, `gateway`. |
| scope | string | - | Required when `device_type` is `ap`. Enum: `network`, `ssid`. |
| is_mld_client | boolean | - | Set to `true` when the client is an MLD client for AP. Default: `false`. |

---
