Return general policy settings plus of a specific network.

### Response Body Example

### Body example
> **Schema illustration only. Values are fictional. Do NOT use as PATCH body base.**
> Always use the actual GET response for the current network state.

```json
{
  "name": "network 1",
  "country": "USA",
  "time_zone": "America/Los_Angeles",
  "custom_ntp_server": {
    "is_enable": false,
    "host": "pool.ntp.org",
    "port": 123
  },
  "local_credential": {
    "username": "admin",
    "password": "admin"
  },
  "local_web_page": {
    "is_enabled": true,
    "is_https_only": false
  },
  "snmp": {
    "mode": "v1_v2c",
    "community_string": "Aa123",
    "configuration": "enabled"
  },
  "snmp_v3": {
    "is_enable": true,
    "users": [
      {
        "username": "public",
        "authorized_key": "12345678",
        "private_key": "12345678",
        "authorized_protocol": "md5",
        "private_protocol": "des"
      },
      {
        "username": "admin",
        "authorized_key": "abcdefgh12345678",
        "private_key": "abcdefgh12345678",
        "authorized_protocol": "sha",
        "private_protocol": "aes"
      }
    ]
  },
  "blocked_message_setting": {
    "is_enable": true,
    "message": "Your device is blocked to access the Wi-Fi network",
    "html": ""
  },
  "blocked_random_mac_setting": {
    "is_enable": false,
    "message": "You are blocked because you turn on random MAC on your devices.",
    "html": ""
  },
  "system_reserved_ip_range": "172.16.0.0/12",
  "is_ap_led_enable": true,
  "is_switch_led_enable": true,
  "is_switch_extender_led_enable": true,
  "is_camera_led_enable": true,
  "is_nvs_led_enable": true,
  "lan_ports": [
    {
      "port": 1,
      "is_enable": true,
      "vlan_mode": "disable",
      "vlan_id": 1,
      "ssid_profile_id": "",
      "is_casting_on_lan_enable": true
    },
    {
      "port": 2,
      "is_enable": true,
      "vlan_mode": "disable",
      "vlan_id": 1,
      "ssid_profile_id": "",
      "is_casting_on_lan_enable": true
    },
    {
      "port": 3,
      "is_enable": true,
      "vlan_mode": "disable",
      "vlan_id": 1,
      "ssid_profile_id": "",
      "is_casting_on_lan_enable": true
    }
  ],
  "lan_ports_by_model": [
    {
      "model_name": "ECW215/115",
      "ports": [
        {
          "port": 1,
          "is_enable": true,
          "vlan_mode": "disable",
          "vlan_id": 1,
          "ssid_profile_id": "",
          "is_casting_on_lan_enable": true
        },
        {
          "port": 2,
          "is_enable": true,
          "vlan_mode": "disable",
          "vlan_id": 1,
          "ssid_profile_id": "",
          "is_casting_on_lan_enable": true
        },
        {
          "port": 3,
          "is_enable": true,
          "vlan_mode": "disable",
          "vlan_id": 1,
          "ssid_profile_id": "",
          "is_casting_on_lan_enable": true
        }
      ]
    },
    {
      "model_name": "ECW515L",
      "ports": [
        {
          "port": 1,
          "is_enable": true,
          "vlan_mode": "disable",
          "vlan_id": 1,
          "ssid_profile_id": "",
          "is_casting_on_lan_enable": true
        },
        {
          "port": 2,
          "is_enable": true,
          "vlan_mode": "disable",
          "vlan_id": 1,
          "ssid_profile_id": "",
          "is_casting_on_lan_enable": true
        },
        {
          "port": 3,
          "is_enable": true,
          "vlan_mode": "disable",
          "vlan_id": 1,
          "ssid_profile_id": "",
          "is_casting_on_lan_enable": true
        },
        {
          "port": 4,
          "is_enable": false,
          "vlan_mode": "disable",
          "vlan_id": 1,
          "ssid_profile_id": "",
          "is_casting_on_lan_enable": true
        },
        {
          "port": 5,
          "is_enable": true,
          "vlan_mode": "disable",
          "vlan_id": 1,
          "ssid_profile_id": "",
          "is_casting_on_lan_enable": false
        }
      ]
    },
    {
      "model_name": "ECW201L",
      "ports": [
        {
          "port": 1,
          "is_enable": true,
          "is_casting_on_lan_enable": true
        },
        {
          "port": 2,
          "is_enable": true,
          "is_casting_on_lan_enable": true
        }
      ]
    }
  ],
  "presence_reporting": {
    "is_enable": true,
    "server_url": "https://123.123.com:8000",
    "key": "test",
    "rate": 5
  },
  "url_recording": {
    "is_enable": true,
    "server_url": "https://123.123.com:8000",
    "key": "test",
    "interval": 5
  },
  "ap_wifi_calling": {
    "is_enable": true,
    "qos_priority": "BestEffort",
    "providers": [
      {
        "name": "domain_server_name",
        "address": "www.senao.com",
        "description": "description"
      },
      {
        "name": "ip_server_name",
        "address": "54.69.179.201",
        "description": "description"
      }
    ]
  },
  "lan_port_settings": {
    "is_link_aggregation_enable": false
  },
  "ap_schedule_reboot": {
    "is_enable": true,
    "schedule_reboots": [
      {
        "is_enable": false,
        "weekday": "sunday",
        "time": "02:10"
      },
      {
        "is_enable": true,
        "weekday": "monday",
        "time": "12:30"
      }
    ]
  },
  "ap_malicious_url_filtering": {
    "is_enable": true,
    "white_list": [
      "1.1.2.2",
      "1.1.2.2:1234",
      "www.white.com"
    ],
    "block_list": [
      "1.2.3.4",
      "1.2.3.4:1234",
      "www.block.com"
    ],
    "external_database": "cht_service"
  },
  "switch_schedule_reboot": {
    "is_enable": false,
    "schedule_reboots": [
      {
        "is_enable": true,
        "weekday": "sunday",
        "time": "05:10"
      },
      {
        "is_enable": false,
        "weekday": "monday",
        "time": "23:30"
      }
    ]
  },
  "is_multicast_to_unicast": true,
  "syslog_server": {
    "is_enable": false,
    "host": "",
    "port": 514,
    "ap": {
      "is_device_log": false,
      "is_traffic_log": false
    },
    "switch": {
      "is_device_log": false
    },
    "switch_extender": {
      "is_device_log": false
    },
    "gateway": {
      "is_device_log": false,
      "is_firewall_log": false,
      "is_traffic_log": false
    },
    "pdu": {
      "is_device_log": false
    }
  },
  "security_event_syslog_server": {
    "is_enable": false,
    "host": "",
    "port": 514
  },
  "is_gateway_lldp_enable": true,
  "nvs_onvif_init_credentials": [
    {
      "num": 1,
      "username": "admin",
      "password": ""
    },
    {
      "num": 2,
      "username": "admin",
      "password": "12345"
    },
    {
      "num": 3,
      "username": "admin",
      "password": "admin"
    },
    {
      "num": 4,
      "username": "root",
      "password": ""
    },
    {
      "num": 5,
      "username": "root",
      "password": "pass"
    }
  ]
}
```

### Response Body Schema

| Field                             | Type          | Description                                        |
| --------------------------------- | ------------- | -------------------------------------------------- |
| name                              | string        | Network name.                                      |
| country                           | string        | Country setting. Must be one of (exact string): Albania, Algeria, Angola, Argentina, Australia, Austria, Bahrain, Belgium, Brazil, Brunei, Bulgaria, Canada, Chile, China, Colombia, Costa Rica, Croatia, Czech Republic, Denmark, Dominican Republic, Ecuador, Egypt, Estonia, Finland, France, Germany, Greece, Guatemala, Honduras, Hong Kong, Hungary, Iceland, India, Indonesia, Iran, Ireland, Israel, Italy, Japan, Jordan, Kazakhstan, Kenya, Kuwait, Latvia, Lebanon, Liechtenstein, Lithuania, Luxembourg, Macau, Malaysia, Mexico, Monaco, Montenegro, Morocco, Myanmar, Nepal, Netherlands, New Zealand, North Macedonia, Norway, Oman, Pakistan, Panama, Peru, Philippines, Poland, Portugal, Puerto Rico, Qatar, Romania, Russia, Saudi Arabia, Singapore, Slovakia, Slovenia, South Africa, South Korea, Spain, Sri Lanka, Sweden, Switzerland, Taiwan, Thailand, Tunisia, Turkey, USA, Ukraine, United Arab Emirates, United Kingdom, Uruguay, Uzbekistan, Venezuela, Vietnam. |
| time_zone                         | string        | Time zone setting.                                 |
| custom_ntp_server                 | object        | NTP server configuration object.                  |
| local_credential                  | object        | Local credential object.                            |
| local_web_page                    | object        | Local web page behavior object.                    |
| snmp                              | object        | SNMP v1/v2c configuration object.                 |
| snmp_v3                           | object        | SNMP v3 configuration object.                     |
| blocked_message_setting           | object        | Blocked-device message object.                    |
| blocked_random_mac_setting        | object        | Random-MAC blocked message object.                |
| system_reserved_ip_range          | string        | Reserved IP range.                                 |
| is_ap_led_enable                  | boolean       | AP LED enabled state.                              |
| is_switch_led_enable              | boolean       | Switch LED enabled state.                          |
| is_switch_extender_led_enable     | boolean       | Switch extender LED enabled state.                 |
| is_camera_led_enable              | boolean       | Camera LED enabled state.                          |
| is_nvs_led_enable                 | boolean       | NVS LED enabled state.                             |
| lan_ports                         | array[object] | Generic LAN port settings list.                   |
| lan_ports_by_model                | array[object] | Model-specific LAN port settings list.             |
| presence_reporting                | object        | Presence reporting object.                         |
| url_recording                     | object        | URL recording object.                              |
| ap_wifi_calling                   | object        | AP Wi-Fi calling object.                           |
| lan_port_settings                 | object        | LAN port advanced settings object.                 |
| ap_schedule_reboot                | object        | AP reboot schedule object.                         |
| ap_malicious_url_filtering        | object        | AP malicious URL filtering object.                 |
| switch_schedule_reboot            | object        | Switch reboot schedule object.                     |
| is_multicast_to_unicast          | boolean       | Multicast-to-unicast behavior flag.               |
| syslog_server                     | object        | Syslog server object.                              |
| security_event_syslog_server       | object        | Security event syslog server object.               |
| is_gateway_lldp_enable            | boolean       | Gateway LLDP enabled state.                        |
| nvs_onvif_init_credentials       | array[object] | Initial ONVIF credential list for NVS.             |

### custom_ntp_server Schema


| Field     | Type    | Description                           |
| --------- | ------- | ------------------------------------- |
| is_enable | boolean | Whether custom NTP server is enabled. |
| host      | string  | NTP server host.                      |
| port      | integer | NTP server port.                      |


### local_credential Schema


| Field    | Type   | Description                |
| -------- | ------ | -------------------------- |
| username | string | Local credential username. |
| password | string | Local credential password. |


### local_web_page Schema


| Field         | Type    | Description                               |
| ------------- | ------- | ----------------------------------------- |
| is_enabled    | boolean | Whether local web page access is enabled. |
| is_https_only | boolean | Whether only HTTPS is allowed.            |


### snmp Schema


| Field            | Type   | Description                |
| ---------------- | ------ | -------------------------- |
| mode             | string | SNMP mode.                 |
| community_string | string | SNMP community string.     |
| configuration    | string | SNMP configuration status. |


### snmp_v3 Schema


| Field     | Type          | Description                 |
| --------- | ------------- | --------------------------- |
| is_enable | boolean       | Whether SNMP v3 is enabled. |
| users     | array[object] | SNMP v3 user list.          |


### snmp_v3 users[] Item Schema


| Field               | Type   | Description                     |
| ------------------- | ------ | ------------------------------- |
| username            | string | SNMP v3 username.               |
| authorized_key      | string | SNMP v3 authorization key.      |
| private_key         | string | SNMP v3 privacy key.            |
| authorized_protocol | string | SNMP v3 authorization protocol. |
| private_protocol    | string | SNMP v3 privacy protocol.       |


### blocked_message_setting Schema


| Field     | Type    | Description                         |
| --------- | ------- | ----------------------------------- |
| is_enable | boolean | Whether blocked message is enabled. |
| message   | string  | Blocked message text.               |
| html      | string  | Blocked message HTML content.       |


### blocked_random_mac_setting Schema


| Field     | Type    | Description                                    |
| --------- | ------- | ---------------------------------------------- |
| is_enable | boolean | Whether random-MAC blocked message is enabled. |
| message   | string  | Random-MAC blocked message text.               |
| html      | string  | Random-MAC blocked message HTML content.       |


### lan_ports[] Item Schema


| Field                    | Type    | Description                        |
| ------------------------ | ------- | ---------------------------------- |
| port                     | integer | Physical LAN port number.          |
| is_enable                | boolean | Whether this LAN port is enabled.  |
| vlan_mode                | string  | VLAN mode for this port.           |
| vlan_id                  | integer | VLAN id for this port.             |
| ssid_profile_id          | string  | Related SSID profile id.           |
| is_casting_on_lan_enable | boolean | Whether casting on LAN is enabled. |


### lan_ports_by_model[] Item Schema


| Field      | Type          | Description                       |
| ---------- | ------------- | --------------------------------- |
| model_name | string        | Device model name.                |
| ports      | array[object] | LAN port settings for this model. |


### presence_reporting Schema


| Field      | Type    | Description                            |
| ---------- | ------- | -------------------------------------- |
| is_enable  | boolean | Whether presence reporting is enabled. |
| server_url | string  | Presence reporting server URL.         |
| key        | string  | Presence reporting key.                |
| rate       | integer | Presence reporting rate.               |


### url_recording Schema


| Field      | Type    | Description                       |
| ---------- | ------- | --------------------------------- |
| is_enable  | boolean | Whether URL recording is enabled. |
| server_url | string  | URL recording server URL.         |
| key        | string  | URL recording key.                |
| interval   | integer | URL recording interval.           |


### ap_wifi_calling Schema


| Field        | Type          | Description                          |
| ------------ | ------------- | ------------------------------------ |
| is_enable    | boolean       | Whether AP Wi-Fi calling is enabled. |
| qos_priority | string        | QoS priority profile name.           |
| providers    | array[object] | Provider entries for Wi-Fi calling.  |


### ap_wifi_calling providers[] Item Schema


| Field       | Type   | Description                |
| ----------- | ------ | -------------------------- |
| name        | string | Provider display name.     |
| address     | string | Provider address value.    |
| description | string | Provider description text. |


### lan_port_settings Schema


| Field                      | Type    | Description                          |
| -------------------------- | ------- | ------------------------------------ |
| is_link_aggregation_enable | boolean | Whether link aggregation is enabled. |


### ap_schedule_reboot Schema


| Field            | Type          | Description                            |
| ---------------- | ------------- | -------------------------------------- |
| is_enable        | boolean       | Whether AP reboot schedule is enabled. |
| schedule_reboots | array[object] | AP reboot schedule list.               |


### switch_schedule_reboot Schema


| Field            | Type          | Description                                |
| ---------------- | ------------- | ------------------------------------------ |
| is_enable        | boolean       | Whether switch reboot schedule is enabled. |
| schedule_reboots | array[object] | Switch reboot schedule list.               |


### schedule_reboots[] Item Schema


| Field     | Type    | Description                             |
| --------- | ------- | --------------------------------------- |
| is_enable | boolean | Whether this schedule entry is enabled. |
| weekday   | string  | Weekday for the schedule entry.         |
| time      | string  | Scheduled time of day.                  |


### ap_malicious_url_filtering Schema


| Field             | Type          | Description                                 |
| ----------------- | ------------- | ------------------------------------------- |
| is_enable         | boolean       | Whether malicious URL filtering is enabled. |
| white_list        | array[string] | Allowed URL/IP entries.                     |
| block_list        | array[string] | Blocked URL/IP entries.                     |
| external_database | string        | External filtering database source.         |


### syslog_server Schema


| Field           | Type    | Description                           |
| --------------- | ------- | ------------------------------------- |
| is_enable       | boolean | Whether syslog forwarding is enabled. |
| host            | string  | Syslog server host.                   |
| port            | integer | Syslog server port.                   |
| ap              | object  | AP syslog options.                    |
| switch          | object  | Switch syslog options.                |
| switch_extender | object  | Switch extender syslog options.       |
| gateway         | object  | Gateway syslog options.                |
| pdu             | object  | PDU syslog options.                   |


### syslog_server ap Schema


| Field          | Type    | Description                            |
| -------------- | ------- | -------------------------------------- |
| is_device_log  | boolean | Whether AP device logs are forwarded.  |
| is_traffic_log | boolean | Whether AP traffic logs are forwarded. |


### syslog_server switch Schema


| Field         | Type    | Description                               |
| ------------- | ------- | ----------------------------------------- |
| is_device_log | boolean | Whether switch device logs are forwarded. |


### syslog_server switch_extender Schema


| Field         | Type    | Description                                        |
| ------------- | ------- | -------------------------------------------------- |
| is_device_log | boolean | Whether switch extender device logs are forwarded. |


### syslog_server gateway Schema


| Field           | Type    | Description                                  |
| --------------- | ------- | -------------------------------------------- |
| is_device_log   | boolean | Whether gateway device logs are forwarded.   |
| is_firewall_log | boolean | Whether gateway firewall logs are forwarded. |
| is_traffic_log  | boolean | Whether gateway traffic logs are forwarded.  |


### syslog_server pdu Schema


| Field         | Type    | Description                            |
| ------------- | ------- | -------------------------------------- |
| is_device_log | boolean | Whether PDU device logs are forwarded. |


### security_event_syslog_server Schema


| Field     | Type    | Description                               |
| --------- | ------- | ----------------------------------------- |
| is_enable | boolean | Whether security event syslog is enabled. |
| host      | string  | Security event syslog server host.        |
| port      | integer | Security event syslog server port.        |


### nvs_onvif_init_credentials[] Item Schema


| Field    | Type    | Description             |
| -------- | ------- | ----------------------- |
| num      | integer | Credential slot number. |
| username | string  | ONVIF username.         |
| password | string  | ONVIF password.         |

### Planner Notes
- Use this API after patch to verify requested field updates.
- GET response does not include `compliance_record`.
