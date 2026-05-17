---
name: network-ap-troubleshoot
description: >
  Troubleshoot AP (Access Point) network devices. Use when the user wants real-time device status,
  client information, network diagnostics (ping, traceroute, speedtest, spectrum scan), or device
  management actions (reboot, factory reset, firmware upgrade, kick clients).
---

## Persona & Output Rules — MANDATORY

⚠️ **Before responding to any user query that triggers this skill**, ensure `../../references/network-admin-persona.md` is loaded into your context:

- **If this is the first persona-aware skill called in this session**: use the **Read tool** to load it now, before any other action.
- **If you've already read persona.md earlier in this session**: you may rely on context (no need to re-read), but you MUST explicitly confirm to yourself which voice principles and escalation rules from persona.md apply to this query before responding.

The file defines voice principles, vocabulary translation (jargon → SMB-friendly), and the escalation matrix (when to reply with text vs dashboard vs action). Without applying it, the response won't match EnGenius brand voice for SMB customers — a product defect.

**Transparency rule**: if the user asks whether you read persona.md, answer honestly (e.g., "loaded earlier in this session, applied from context" vs "just loaded via Read tool").

# AP Network Troubleshoot

## API Operations

### subscribe_spectrum_scan
- description: Subscribe to real-time spectrum scan data for a specific band (not supported on Dakota platform)

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_spectrum_scan.md`.

### subscribe_stat
- description: Subscribe to real-time device statistics (CPU, memory)

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_stat.md`.

### subscribe_throughput
- description: Subscribe to real-time throughput data for a specific band (unit: B/s)

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_throughput.md`.

### subscribe_channel_utilization
- description: Subscribe to real-time channel utilization for a specific band

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_channel_utilization.md`.

### subscribe_all_channel_utilization
- description: Subscribe to all channel utilization data for a specific band

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_all_channel_utilization.md`.

### subscribe_client_list
- description: Subscribe to real-time client list for specified MAC addresses; supports MLD clients (WiFi 7/BE)

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_client_list.md`.

### subscribe_speedtest
- description: Subscribe to real-time speedtest results

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_speedtest.md`.

### subscribe_ping
- description: Subscribe to real-time ping results for a target host

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_ping.md`.

### subscribe_traceroute
- description: Subscribe to real-time traceroute results for a target host

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_traceroute.md`.

### rpc_speedtest_serverlist
- description: Get available speedtest server list

#### Request Body

> Full request body schema and example: see API schema `references/rpc_speedtest_serverlist.md`.

### rpc_wifi_scan
- description: Scan WiFi channels on all bands or a specific band

#### Request Body

> Full request body schema and example: see API schema `references/rpc_wifi_scan.md`.

### rpc_all_chan_util
- description: Get channel utilization for all channels on a specific band or all bands

#### Request Body

> Full request body schema and example: see API schema `references/rpc_all_chan_util.md`.

### rpc_client_info_list
- description: Get detailed client info with optional SSID profile and band filter

#### Request Body

> Full request body schema and example: see API schema `references/rpc_client_info_list.md`.

### rpc_file_upload
- description: Upload a file (e.g., WIDS record) from AP to a pre-signed URL

#### Request Body

> Full request body schema and example: see API schema `references/rpc_file_upload.md`.

### rpc_reboot
- description: Reboot the AP device

#### Request Body

> Full request body schema and example: see API schema `references/rpc_reboot.md`.

### rpc_checkin
- description: Force a check-in on the AP device

#### Request Body

> Full request body schema and example: see API schema `references/rpc_checkin.md`.

### rpc_upgrade
- description: Upgrade firmware on the AP device (4-digit version)

#### Request Body

> Full request body schema and example: see API schema `references/rpc_upgrade.md`.

### rpc_meshautopairing
- description: Trigger automatic mesh pairing

#### Request Body

> Full request body schema and example: see API schema `references/rpc_meshautopairing.md`.

### rpc_failsafe_upgrade
- description: Upgrade failsafe firmware on the AP device (3-digit version)

#### Request Body

> Full request body schema and example: see API schema `references/rpc_failsafe_upgrade.md`.

### rpc_kick_clients
- description: Disconnect specified clients from the AP

#### Request Body

> Full request body schema and example: see API schema `references/rpc_kick_clients.md`.

### rpc_ssh_tunnel
- description: Establish SSH tunnel to an AP device

#### Request Body

> Full request body schema and example: see API schema `references/rpc_ssh_tunnel.md`.

### rpc_led_dance
- description: Trigger LED dance on AP device for physical identification

#### Request Body

> Full request body schema and example: see API schema `references/rpc_led_dance.md`.

### rpc_factory_reset
- description: Factory reset the AP device

#### Request Body

> Full request body schema and example: see API schema `references/rpc_factory_reset.md`.

### rpc_ext_config_download
- description: Download external config file to the AP (e.g., URL filtering config or Lionic signature)

#### Request Body

> Full request body schema and example: see API schema `references/rpc_ext_config_download.md`.

### rpc_radius_coa
- description: Send Radius Change of Authorization (COA) or Disconnect request to kick clients by username or MAC

#### Request Body

> Full request body schema and example: see API schema `references/rpc_radius_coa.md`.

## Flow Modules (Execution Order)

Use the following flow modules in order. Keep each module independent, so adding a new module does not change existing module behavior unless explicitly stated.

### F0. Prerequisite Gate (Identifier Resolution)

1. If required ids are missing, resolve in this order:
   - Load skill `orgs`, then invoke `get_user_orgs` to resolve canonical `orgId`.
   - Invoke `get_inventory` with resolved `orgId` to discover devices and their `network_id`, `mac`, and `network_name`.
   - Use user-provided names only as lookup hints; never fabricate IDs.
2. From the inventory response, identify the target AP device and resolve both its `mac` and `network_id`.
3. Pass `device_mac` (the resolved MAC address) as a required parameter to every `subscribe_*` and `rpc_*` operation.

### F1. Connectivity Check

1. After F0 passes and `network_id` is resolved, invoke `subscribe_ping` with `host: "8.8.8.8"` to verify the AP has external connectivity.
2. If ping fails or returns no data, stop and report to the user that the device cannot reach the internet. Do not proceed to speedtest.

### F2. Speedtest Server Discovery

1. Invoke `rpc_speedtest_serverlist` to retrieve available speedtest servers.
2. If the server list is empty, stop and report to the user that no speedtest servers are available.

### F3. Speedtest Execution

1. Invoke `subscribe_speedtest` to run the speedtest on the AP device.
2. Report download/upload speeds to the user.

### F4. Completion Convergence

1. After speedtest completes, stop and respond to the user with:
   - Ping result summary (connectivity confirmed)
   - Speedtest server used
   - Download speed and upload speed

### F5. API Naming and Reference Rule

1. When invoking an API operation, use only the plain `operation_id` as defined in the `## API Operations` section above.
2. If request or response schema detail is unclear, load the reference schema from `references/<operation_id>.md`.

## Constraints (Hard Rules)

These constraints are independent from flow modules. New constraints should be appended as new `C*` items without rewriting existing ones.

- C1 Network ID guard:
  - All troubleshoot operations require a valid `network_id` resolved from `get_inventory`.
  - Never fabricate or guess `network_id`. If not resolved, do not invoke any troubleshoot operation.
- C2 Connectivity prerequisite:
  - `subscribe_speedtest` and `rpc_speedtest_serverlist` must not be invoked unless connectivity has been verified (ping check passed) or the user explicitly skips the check.
- C3 Platform note:
  - `subscribe_spectrum_scan` is not supported on Dakota platform APs. Check device compatibility before invoking.
- C4 MAC guard:
  - All `subscribe_*` and `rpc_*` operations require `device_mac` resolved from `get_inventory`.
  - Never fabricate or guess `device_mac`. Always pass the exact MAC from the inventory device entry.
