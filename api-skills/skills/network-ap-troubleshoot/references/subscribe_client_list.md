- description: Subscribe to real-time client list for specified MAC addresses; supports MLD clients (WiFi 7/BE)

### Request Body Schema

| Field | Type | Required | Description |
|---|---|---|---|
| network_id | string | true | Target network identifier |
| device_mac | string | true | Device MAC address from inventory |
| macs | array | false | List of client MAC addresses to filter |

### Request Body Example

```json
{
    "network_id": "68ff2d8d5c048e7e2f7d3077",
    "macs": ["00:11:22:33:44:55"]
}
```

### Internal Subscribe Format

```json
{
    "topic": "client_list",
    "options": {
        "macs": ["00:11:22:33:44:55"]
    }
}
```

### Response Body Example

```json
{
    "topic": "client_list",
    "device": "88:dc:96:84:e1:67",
    "content": {
        "client_list": [
            {
                "mac": "2a:d1:3f:70:65:22",
                "mld_mac": "00:11:11:11:11:11",
                "rssi": -46,
                "snr": 33,
                "identity": "username",
                "protocol": "AX",
                "band": "5GHz",
                "rate": 680,
                "ip": "172.25.0.26",
                "device_name": "yu-chen-de-Galaxy-Note20-Ultra-",
                "os": "Android",
                "stat": 1,
                "update_time": 1619517450776,
                "ssid_name": "EnGenius_ssid1",
                "down": 502784,
                "up": 70656,
                "tx": 6367,
                "rx": 636,
                "idle": 22,
                "assoc_time": "00:33:58",
                "vlan_id": 0
            }
        ]
    }
}
```

### Field Notes

- `down`/`up`: Reset to zero every 5 minutes; use `tx`/`rx` for current traffic
- `tx`/`rx`: Current traffic, unit: Kbytes
- `snr`: Unit: dB
- `idle`: Unit: seconds; client is kicked by AP if idle > 300s
- `mld_mac`: Only present when the client is an MLD client (WiFi 7/BE)
- `identity`: 802.1X username if applicable

### Update Triggers

1. Any client connects → delayed 8 seconds
2. Any client disconnects → immediate
3. Otherwise → every 6 seconds
