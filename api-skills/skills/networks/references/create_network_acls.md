Add a client to the Network/AP/Gateway ACL blocklist, allowlist, or VIP client list. MLD client creation is not supported.

### Request Body Example

#### Network

```json
{
  "description": "Client 1",
  "mac": "88:dc:96:79:f2:cc",
  "scope": "network",
  "access": "vip",
  "device_type": "ap"
}
```
#### AP/SSID Profile
```json
{
  "description": "Client 2",
  "mac": "88:dc:96:79:f2:cd",
  "scope": "ssid",
  "access": "block",
  "ssid_profile_ids": ["5e5df1e1322204f7b0708ea8"],
  "device_type": "ap"
}
```
#### Gateway
```json
{
  "description": "Client 3",
  "mac": "88:dc:96:79:f2:cc",
  "access": "white",
  "device_type": "gateway"
}
```

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| mac | string | ✅ | Client MAC address (format: `xx:xx:xx:xx:xx:xx`). MLD MAC is not supported. |
| access | string | ✅ | ACL type: `block`, `white`, or `vip`. |
| scope | string | - | Applies only when `device_type` is `ap`. Enum: `network`, `ssid`. |
| description | string | - | Description (comment) of the ACL rule. |
| ssid_profile_ids | array[string] | - | Required (min 1 item) when `scope` is `ssid`. |
| device_type | string | - | Device type of the ACL rule. Enum: `ap`, `gateway`. Default: `ap`. |

### Input Validation Notes (Pre-check Before API Call)

- Validate `mac` before sending request.
- Accepted format: `xx:xx:xx:xx:xx:xx` (lowercase hex, colon-separated, 6 octets).
- Normalise common user inputs:
  - `88DC9679F2CC` → `88:dc:96:79:f2:cc` (insert colons, lowercase)
  - `88-DC-96-79-F2-CC` → `88:dc:96:79:f2:cc` (replace dashes, lowercase)
  - `88:DC:96:79:F2:CC` → `88:dc:96:79:f2:cc` (lowercase)
- If the input cannot be parsed into a valid 6-octet MAC, do not call API. Return a user-facing validation error directly.

### Planner Notes — Scope Selection

There are exactly three scope variants. Each maps to a different request body shape:

| User intent (UI equivalent) | `device_type` | `scope` | `ssid_profile_ids` | Body format |
| ---------------------------- | ------------- | ------- | ------------------- | ----------- |
| Wireless → **All SSIDs** | `ap` | `network` | omit | Network |
| Wireless → **specific SSID(s)** | `ap` | `ssid` | required (≥1) | AP/SSID Profile |
| **Gateway** → All LAN Interfaces | `gateway` | omit | omit | Gateway |

- If the user says "block on wireless" or "block on AP" without specifying All SSIDs vs specific SSID(s), stop and ask the user to clarify which scope before building the body.
- If the user names specific SSID(s), use **AP/SSID Profile** format: set `scope: "ssid"` and resolve names to ids via `get_ssid_profiles`.
- If the user says "all SSIDs" / "整個網路" / "全部 SSID", use **Network** format: set `scope: "network"`, omit `ssid_profile_ids`.
- If the user says "gateway" / "LAN", use **Gateway** format: set `device_type: "gateway"`, omit `scope` and `ssid_profile_ids`.

---
