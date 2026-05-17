Return the ACL blocklist, allowlist, or VIP client list in the Network/AP/Gateway.

### Response Body Example

```json
{
  "clients": [
    {
      "description": "client 1",
      "mac": "00:11:aa:bb:cc:dd",
      "is_mld_client": false,
      "mac_list": [],
      "scope": "network",
      "device_name": "test client 1",
      "device_type": "ap",
      "original_device_name": "client A"
    },
    {
      "mac": "01:11:aa:bb:cc:ea",
      "is_mld_client": true,
      "mac_list": ["02:11:aa:bb:cc:eb", "03:11:aa:bb:cc:ec"],
      "scope": "ssid",
      "device_name": "test client 2",
      "device_type": "ap",
      "original_device_name": "client B",
      "ssid_profiles": [
        {
          "id": "5e5df1e1322204f7b0708ea8",
          "name": "ezmcloud",
          "description": "client 2"
        }
      ]
    },
    {
      "description": "client 3",
      "mac": "00:11:aa:bb:cc:dd",
      "device_name": "test client 3",
      "device_type": "gateway",
      "original_device_name": "client A"
    }
  ],
  "size": 10,
  "is_devices_over_clients_limitation": false
}
```

### Response Body Schema

| Field | Type | Description |
|---|---|---|
| clients | array[object] | List of ACL client entries. |
| size | integer | Total number of ACL clients in the database. |
| is_devices_over_clients_limitation | boolean | If `true`, the number of devices has exceeded the limit. |

### clients[] Item Schema

| Field | Type | Description |
|---|---|---|
| mac | string | Client MAC address. When `is_mld_client` is `true`, this is the `mld_mac_addr`. |
| is_mld_client | boolean | If `true`, the client is an MLD client for AP. |
| mac_list | array[string] | Only populated when `is_mld_client` is `true`. |
| scope | string | ACL scope when `device_type` is `ap`. Enum: `network`, `ssid`. |
| description | string | Description (comment) of the ACL rule. |
| device_name | string | The name of the device. |
| original_device_name | string | The original name of the device. |
| device_type | string | Device type of the ACL rule. Enum: `ap`, `gateway`. |
| ssid_profiles | array[object] | Only provided when `scope` is `ssid`. |

### ssid_profiles[] Item Schema

| Field | Type | Description |
|---|---|---|
| id | string | The ID of the SSID profile. |
| name | string | The name of the SSID profile. |
| description | string | The description of the SSID profile. |

---
