Retrieves a list of all SSID profiles in the network with optional filtering capabilities.

### Response Body Example

> **Schema illustration only. Values are fictional. Do NOT use as PATCH body base.**
> Always use the actual GET response for the current network state.


```json
[
  {
    "id": "57185d926c8051e28e03ec90ba5",
    "ssid_name": "SSID_1",
    "ssid_category": "General",
    "is_enable": true,
    "is_used_by_lan_ports": false,
    "ssid_types": [
      {
        "id": 0,
        "type": "2_4G",
        "is_enable": true
      },
      {
        "id": 1,
        "type": "5G",
        "is_enable": true
      },
      {
        "id": 2,
        "type": "6G",
        "is_enable": true
      }
    ],
    "is_emergency_wifi": false,
    "is_hidden": false,
    "is_client_isolation": false,
    "is_l2_isolation": false,
    "is_vlan_isolation": false,
    "is_bcmc_suppression": true,
    "is_mld_enable": false,
    "vlan_id": null,
    "is_fast_roaming": false,
    "is_mdns_forward": false,
    "is_acl_enable": false,
    "ieee_802_11w": {
      "is_enable": true,
      "mode": "11w_client_only"
    },
    "client_ip_assignment": "bridge",
    "client_custom_dns_server": {
      "is_enable": false,
      "primary_dns": null,
      "secondary_dns": null
    },
    "band_steering": {
      "is_enable": false,
      "type": "prefer_5g",
      "rssi_threshold_5g": -75,
      "client_percent_5g": 75
    },
    "is_app_detection": true,
    "traffic_shaping": {
      "is_enable": false,
      "is_perssid_limit_enable": false,
      "perssid_download_limit": 100,
      "perssid_upload_limit": 100,
      "is_perclient_limit_enable": false,
      "perclient_download_limit": 5,
      "perclient_upload_limit": 5,
      "app_rate_limit": {
        "is_enable": false,
        "applications": {
          "voice_calls": "express",
          "video_conference": "general",
          "streaming": "general",
          "online_gaming": "general",
          "others": "general"
        }
      }
    },
    "security": {
      "auth_type": "OWE",
      "dynamic_vlan": {
        "is_enable": false,
        "vlan_pool": null
      },
      "wpa": {
        "type": "aes",
        "interval": 3600,
        "passphrase": null,
        "mypsk": {
          "auth_type": "cloud",
          "is_enable": false
        }
      }
    },
    "captive_portal": {
      "is_enable": false,
      "auth_type": "click-through",
      "splash_page_type": "internal",
      "external_splash_url": null,
      "after_splash_redirect_url": null,
      "enable_redirect_client_track": true,
      "is_start_counting_after_first_login": false,
      "is_send_frontdesk_notification": false,
      "is_redirect_ssl_enable": true,
      "session_timeout": 60,
      "idle_timeout": 30,
      "is_https_login_enable": true,
      "walled_garden": [],
      "is_traffic_control_by_radius": false,
      "is_radius_mac_auth": false,
      "splash_page_walled_garden": [],
      "facebook_wifi_auth_url": null
    },
    "radius_server": {
      "type": "custom_radius",
      "auth_type": "chap",
      "retries": 4,
      "server_1_ip": null,
      "server_1_port": 1812,
      "server_1_secret": null,
      "server_2_ip": null,
      "server_2_port": null,
      "server_2_secret": null,
      "suite_b": false,
      "is_coa_enable": false,
      "is_vlan_control_by_radius": false,
      "is_server_1_tls": false,
      "is_server_2_tls": false
    },
    "radius_setting": {
      "is_nas_id": false,
      "nas_id": null,
      "is_nas_ip": false,
      "nas_ip": null,
      "is_nas_port": false,
      "nas_port": null
    },
    "is_enable_accounting": false,
    "accounting_server": {
      "interval": 600,
      "server_1_ip": null,
      "server_1_port": null,
      "server_1_secret": null,
      "server_2_ip": null,
      "server_2_port": null,
      "server_2_secret": null,
      "is_server_1_tls": false,
      "is_server_2_tls": false
    },
    "scheduling": {
      "is_enable": false,
      "schedules": []
    },
    "slot_id": 1,
    "hotspot20": {
      "is_enable": false,
      "operator_name": null,
      "general_settings": {
        "venue_name": null,
        "venue_group": 0,
        "venue_type": 0,
        "network_type": 0,
        "advanced_settings": {
          "hessid": null,
          "network_auth_type": 0,
          "redirect_url": null
        }
      },
      "domain_list": [],
      "roaming_consortium_list": [],
      "anqp_3gpp_cellular_network_info": [],
      "nai_realms": []
    },
    "is_ssid_for_lite_enabled": true
  }
]
```

### Query Parameters

| Name               | Type    | Description |
| ------------------ | ------- | ----------- |
| constrain          | string  | Optional. `usable_by_lan_ports` — only SSIDs assignable to LAN ports. Omit or use empty string for all. |
| ssid_name          | string  | Optional. Case-insensitive partial match on SSID name. |
| is_emergency_wifi  | boolean | Optional. Filter by emergency WiFi flag. |

### Response Body Schema

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | string | SSID profile ID. |
| slot_id | integer | Slot index. |
| ssid_name | string | SSID broadcast name. |
| ssid_category | string | `General` \| `SmartTV`. |
| is_enable | boolean | SSID enabled. |
| is_used_by_lan_ports | boolean | Used by LAN port assignment. |
| ssid_types | array | Per-band enable; see **ssid_types[]** table. |
| is_emergency_wifi | boolean | Emergency WiFi profile. |
| is_hidden | boolean | Hidden SSID. |
| is_client_isolation | boolean | Client isolation. |
| is_l2_isolation | boolean | L2 isolation. |
| is_vlan_isolation | boolean | VLAN isolation. |
| is_bcmc_suppression | boolean | Broadcast/multicast suppression. |
| is_mld_enable | boolean | MLD (IPv6 multicast) enable. |
| vlan_id | integer \| null | VLAN ID when applicable. |
| is_fast_roaming | boolean | Fast roaming (802.11r). |
| is_mdns_forward | boolean | mDNS forwarding. |
| is_acl_enable | boolean | ACL (block/VIP/whitelist) feature enabled. |
| is_ssid_for_lite_enabled | boolean | Enabled for Cloud-Lite devices (default true in schema). |
| ieee_802_11w | object | Management frame protection; see **ieee_802_11w**. |
| client_ip_assignment | string | `bridge` \| `nat` \| `eogre`. |
| client_custom_dns_server | object | Custom DNS for clients; see **client_custom_dns_server**. |
| band_steering | object | See **band_steering**. |
| is_app_detection | boolean | Application detection. |
| traffic_shaping | object | See **traffic_shaping**. |
| security | object | Auth summary; see **security (list item)**. |
| captive_portal | object | See **captive_portal**. |
| radius_server | object | RADIUS auth servers; see **radius_server (list)**. |
| radius_setting | object | NAS ID/IP/port overrides; see **radius_setting**. |
| is_enable_accounting | boolean | RADIUS accounting on. |
| accounting_server | object | Accounting servers; see **accounting_server**. |
| scheduling | object | SSID schedule; see **scheduling**. |
| hotspot20 | object | Passpoint / Hotspot 2.0; see **hotspot20**. |

#### ssid_types[]

| Field | Type | Description |
| ----- | ---- | ----------- |
| id | integer | Band slot id (e.g. 0, 1, 2). |
| type | string | e.g. `2_4G`, `5G`, `6G`. |
| is_enable | boolean | That band enabled for this SSID. |

#### ieee_802_11w

| Field | Type | Description |
| ----- | ---- | ----------- |
| is_enable | boolean | 802.11w enabled. |
| mode | string | `all_clients` \| `11w_client_only`. |

#### client_custom_dns_server

| Field | Type | Description |
| ----- | ---- | ----------- |
| is_enable | boolean | Use custom DNS. |
| primary_dns | string \| null | Primary DNS (IPv4 pattern when set). |
| secondary_dns | string \| null | Secondary DNS. |

#### band_steering

| Field | Type | Description |
| ----- | ---- | ----------- |
| is_enable | boolean | Band steering on. |
| type | string | Steering mode (e.g. `prefer_5g`). |
| rssi_threshold_5g | integer | 5 GHz RSSI threshold. |
| client_percent_5g | integer | Target % on 5 GHz. |

#### traffic_shaping

| Field | Type | Description |
| ----- | ---- | ----------- |
| is_enable | boolean | Traffic shaping on. |
| is_perssid_limit_enable | boolean | Per-SSID rate limit. |
| perssid_download_limit | integer | SSID download limit (Mbps class unit per API). |
| perssid_upload_limit | integer | SSID upload limit. |
| is_perclient_limit_enable | boolean | Per-client limit. |
| perclient_download_limit | integer | Per-client download. |
| perclient_upload_limit | integer | Per-client upload. |
| app_rate_limit | object | App-class limits; see **app_rate_limit.applications**. |

#### app_rate_limit

| Field | Type | Description |
| ----- | ---- | ----------- |
| is_enable | boolean | Application-based limits on. |
| applications | object | See **traffic_shaping.applications**. |

#### traffic_shaping.applications

| Field | Type | Description |
| ----- | ---- | ----------- |
| voice_calls | string | `express`. |
| video_conference | string | `general` \| `fast` \| `express`. |
| streaming | string | `general` \| `fast` \| `express`. |
| online_gaming | string | `general` \| `fast` \| `express`. |
| others | string | `general`. |

#### security (list item)

| Field | Type | Description |
| ----- | ---- | ----------- |
| auth_type | string | `disabled` \| `WPA/WPA2-PSK` \| `WPA2-PSK` \| `WPA2-Enterprise` \| `OWE` \| `WPA3-Personal` \| `WPA2/WPA3-Personal` \| `WPA3-Enterprise`. |
| dynamic_vlan | object | See **dynamic_vlan**. |
| wpa | object | See **wpa (list security)**. |

#### dynamic_vlan

| Field | Type | Description |
| ----- | ---- | ----------- |
| is_enable | boolean | Dynamic VLAN from RADIUS. |
| vlan_pool | string \| null | VLAN id pool expression. |

#### wpa (list security)

| Field | Type | Description |
| ----- | ---- | ----------- |
| type | string | e.g. `aes`. |
| interval | integer | Key rotation interval (seconds). |
| passphrase | string \| null | PSK when applicable. |
| mypsk | object | Cloud/custom PSK: `auth_type` (`cloud` \| `custom`), `is_enable`. |

#### captive_portal

| Field | Type | Description |
| ----- | ---- | ----------- |
| is_enable | boolean | Captive portal on. |
| auth_type | string | e.g. `click-through`, `engenius_radius`, `cloud_radius`, `custom_radius`, `3rd_party`, `hot-spot`, `social_login`, `facebook_wifi`, `google_ldap`, `azure_ad_ldap`, `azure_ad_saml`, `ldap`, `active_directory`. |
| splash_page_type | string | `internal` \| `external` (when validated). |
| external_splash_url | string \| null | External splash URL. |
| after_splash_redirect_url | string \| null | Post-login redirect. |
| enable_redirect_client_track | boolean | Track client after redirect. |
| is_start_counting_after_first_login | boolean | Session counting mode. |
| is_send_frontdesk_notification | boolean | Front-desk notification. |
| is_redirect_ssl_enable | boolean | Redirect over SSL. |
| session_timeout | integer | Session timeout (minutes). |
| idle_timeout | integer | Idle timeout (minutes). |
| is_https_login_enable | boolean | HTTPS login page. |
| walled_garden | array | Allowed destinations (host/IP patterns). |
| is_traffic_control_by_radius | boolean | RADIUS-driven traffic control. |
| is_radius_mac_auth | boolean | MAC auth via RADIUS. |
| splash_page_walled_garden | array | Walled garden for splash. |
| facebook_wifi_auth_url | string \| null | Facebook WiFi pairing URL when relevant. |
| facebook_wifi_page_name | string \| null | |
| facebook_wifi_page_link | string \| null | |
| is_facebook_wifi_paired | boolean | |
| ldap_base_dn | string \| null | |
| ldap_login_attribute | string | |

#### radius_server (list)

Extends base RADIUS server fields plus load balance.

| Field | Type | Description |
| ----- | ---- | ----------- |
| type | string | e.g. `custom_radius`. |
| auth_type | string | e.g. `chap`. |
| retries | integer | Retry count. |
| server_1_ip | string \| null | Primary auth IP. |
| server_1_port | integer \| null | Primary port (e.g. 1812). |
| server_1_secret | string \| null | Shared secret. |
| server_2_ip | string \| null | Secondary auth IP. |
| server_2_port | integer \| null | |
| server_2_secret | string \| null | |
| suite_b | boolean | Suite B crypto. |
| is_coa_enable | boolean | CoA. |
| is_vlan_control_by_radius | boolean | VLAN from RADIUS. |
| is_server_1_tls | boolean | TLS to server 1. |
| is_server_2_tls | boolean | TLS to server 2. |
| is_server_3_tls | boolean | TLS to server 3 (if present on other variants). |
| is_load_balance | boolean | Load balance across servers (list schema). |

#### radius_setting

| Field | Type | Description |
| ----- | ---- | ----------- |
| is_nas_id | boolean | Send NAS-ID. |
| nas_id | string \| null | NAS-Identifier. |
| is_nas_ip | boolean | Send NAS-IP. |
| nas_ip | string \| null | |
| is_nas_port | boolean | Send NAS-Port. |
| nas_port | integer \| null | |

#### accounting_server

| Field | Type | Description |
| ----- | ---- | ----------- |
| interval | integer | Interim update interval (seconds). |
| server_1_ip | string \| null | |
| server_1_port | integer \| null | |
| server_1_secret | string \| null | |
| server_2_ip | string \| null | |
| server_2_port | integer \| null | |
| server_2_secret | string \| null | |
| is_load_balance | boolean | |
| is_server_1_tls | boolean | |
| is_server_2_tls | boolean | |
| is_server_3_tls | boolean | |

#### scheduling

| Field | Type | Description |
| ----- | ---- | ----------- |
| is_enable | boolean | Time-based SSID on/off. |
| schedules | array | See **scheduling.schedules[]**. |

#### scheduling.schedules[]

| Field | Type | Description |
| ----- | ---- | ----------- |
| week_day | string | `monday` … `sunday`. |
| is_available | boolean | SSID available that day. |
| start_time | string | Start time (HH:MM). |
| end_time | string | End time (HH:MM). |

#### hotspot20

| Field | Type | Description |
| ----- | ---- | ----------- |
| is_enable | boolean | Hotspot 2.0 / Passpoint on. |
| operator_name | string \| null | Operator name (pattern/length per OpenAPI). |
| general_settings | object | Venue/network identity; see **hotspot20.general_settings**. |
| domain_list | array[string] | Domain list (max 8, URL format). |
| roaming_consortium_list | array[string] | Hex OI strings (max 16). |
| anqp_3gpp_cellular_network_info | array | Cellular network ANQP; see **anqp_3gpp_cellular_network_info[]**. |
| nai_realms | array | NAI realms; see **nai_realms[]**. |

#### hotspot20.general_settings

| Field | Type | Description |
| ----- | ---- | ----------- |
| venue_name | string \| null | |
| venue_group | integer | 0–11 (venue group enum; see liveapi schema). |
| venue_type | integer | 0–15 (venue type within group; see liveapi long enum). |
| network_type | integer | 0–5, 14, 15 (private / public / emergency / test / wildcard). |
| advanced_settings | object | See **hotspot20.advanced_settings**. |

#### hotspot20.advanced_settings

| Field | Type | Description |
| ----- | ---- | ----------- |
| hessid | string \| null | Homogeneous ESS identifier (MAC or empty). |
| network_auth_type | integer | `0` terms acceptance \| `2` http/https redirect. |
| redirect_url | string \| null | Redirect URL when applicable. |

#### anqp_3gpp_cellular_network_info[]

| Field | Type | Description |
| ----- | ---- | ----------- |
| mobile_country_code | string | 3 digits. |
| mobile_network_code | string | 2–3 digits. |

#### nai_realms[]

| Field | Type | Description |
| ----- | ---- | ----------- |
| format | integer | 0 or 1. |
| name | string | Realm name (1–255 chars, pattern per OpenAPI). |
| methods | array | Up to 4 entries; see **nai_realm.methods[]**. |

#### nai_realm.methods[]

| Field | Type | Description |
| ----- | ---- | ----------- |
| method_id | integer | EAP method id. Allowed values: 0–55, 254, 255 (see enum below). |
| auth_method_group | integer | Auth parameter group. `2` = Non-EAP Inner Auth Type, `5` = Credential Type, `6` = Tunneled EAP Method Credential Type. |
| auth_method_type | integer | Auth value (0–10). Meaning depends on `auth_method_group` (see table below). |
