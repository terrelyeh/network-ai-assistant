---
name: network-gateway-troubleshoot
description: >
  Troubleshoot Gateway network devices. Use when the user wants real-time gateway status,
  WAN diagnostics (ping, traceroute, speedtest, throughput), port statistics, VPN peer
  status, HA status, or gateway management actions (PoE reset, external config download).
---

## Persona & Output Rules — MANDATORY

⚠️ **Before responding to any user query that triggers this skill**, ensure `../../references/network-admin-persona.md` is loaded into your context:

- **If this is the first persona-aware skill called in this session**: use the **Read tool** to load it now, before any other action.
- **If you've already read persona.md earlier in this session**: you may rely on context (no need to re-read), but you MUST explicitly confirm to yourself which voice principles and escalation rules from persona.md apply to this query before responding.

The file defines voice principles, vocabulary translation (jargon → SMB-friendly), and the escalation matrix (when to reply with text vs dashboard vs action). Without applying it, the response won't match EnGenius brand voice for SMB customers — a product defect.

**Transparency rule**: if the user asks whether you read persona.md, answer honestly (e.g., "loaded earlier in this session, applied from context" vs "just loaded via Read tool").

# Gateway Network Troubleshoot

## API Operations

### subscribe_stat
- description: Subscribe to real-time gateway device statistics (CPU, memory)

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_stat.md`.

### subscribe_throughput
- description: Subscribe to real-time WAN interface throughput (unit: B/s); supports WAN1, WAN2, WWAN

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_throughput.md`.

### subscribe_ping
- description: Subscribe to real-time ping results for a target host; supports source interface selection

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_ping.md`.

### subscribe_speedtest
- description: Subscribe to real-time speedtest results; supports server and source interface selection

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_speedtest.md`.

### subscribe_traceroute
- description: Subscribe to real-time traceroute results; supports interface and IP version (v4/v6) selection

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_traceroute.md`.

### subscribe_vpnpeer_status
- description: Subscribe to real-time VPN peer status (PRO feature)

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_vpnpeer_status.md`.

### subscribe_port_stat
- description: Subscribe to real-time gateway port statistics (gateway v1.2.85+)

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_port_stat.md`.

### subscribe_ha_info
- description: Subscribe to real-time HA (High Availability) status (gateway v1.2.85+)

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_ha_info.md`.

### rpc_speedtest_serverlist
- description: Get available speedtest server list

#### Request Body

> Full request body schema and example: see API schema `references/rpc_speedtest_serverlist.md`.

### rpc_poe_reset
- description: Reset a PoE port on the gateway device

#### Request Body

> Full request body schema and example: see API schema `references/rpc_poe_reset.md`.

### rpc_ext_config_download
- description: Download external config file to the gateway (e.g., URL filtering config or Lionic signature)

#### Request Body

> Full request body schema and example: see API schema `references/rpc_ext_config_download.md`.

### download_packet_file
- description: Download a packet capture file from a specified WAN interface (PRO feature, gateway v1.2.45+)

#### Request Body

> Full request body schema and example: see API schema `references/download_packet_file.md`.

### download_firewall_log
- description: Download a real-time firewall log file filtered by rule type (gateway v1.2.50+)

#### Request Body

> Full request body schema and example: see API schema `references/download_firewall_log.md`.

### download_esg_root_ca
- description: Download the ESG Root CA certificate from the gateway (gateway v1.2.85+)

#### Request Body

> Full request body schema and example: see API schema `references/download_esg_root_ca.md`.

### download_esg_eap_cert
- description: Download an ESG EAP client certificate for a specific user email (gateway v1.2.100+)

#### Request Body

> Full request body schema and example: see API schema `references/download_esg_eap_cert.md`.

## Flow Modules (Execution Order)

Use the following flow modules in order. Keep each module independent, so adding a new module does not change existing module behavior unless explicitly stated.

### F0. Prerequisite Gate (Identifier Resolution)

1. If required ids are missing, resolve in this order:
   - Load skill `orgs`, then invoke `get_user_orgs` to resolve canonical `orgId`.
   - Invoke `get_inventory` with resolved `orgId` to discover devices and their `network_id`, `mac`, and `network_name`.
   - Use user-provided names only as lookup hints; never fabricate IDs.
2. From the inventory response, identify the target gateway device and resolve both its `mac` and `network_id`.
3. Pass `device_mac` (the resolved MAC address) as a required parameter to every `subscribe_*` and `rpc_*` operation.

### F1. Connectivity Check

1. After F0 passes and `network_id` is resolved, invoke `subscribe_ping` with `host: "8.8.8.8"` to verify the gateway has external connectivity.
2. If ping fails or returns no data, stop and report to the user that the device cannot reach the internet. Do not proceed to speedtest.

### F2. Speedtest Server Discovery

1. Invoke `rpc_speedtest_serverlist` to retrieve available speedtest servers.
2. If the server list is empty, stop and report to the user that no speedtest servers are available.

### F3. Speedtest Execution

1. Invoke `subscribe_speedtest` to run the speedtest on the gateway device.
2. Report download/upload speeds to the user.

### F4. Completion Convergence

1. After speedtest completes, stop and respond to the user with:
   - Ping result summary (connectivity confirmed)
   - Speedtest server used
   - Download speed and upload speed

### F5. API Naming and Reference Rule

1. When invoking an API operation, use only the plain `operation_id` as defined in the `## API Operations` section above.
2. Operation prefixes: `subscribe_*` for SSE streaming, `rpc_*` for RPC calls, `download_*` for file download.
3. If request or response schema detail is unclear, load the reference schema from `references/<operation_id>.md`.

## Constraints (Hard Rules)

These constraints are independent from flow modules. New constraints should be appended as new `C*` items without rewriting existing ones.

- C1 Network ID guard:
  - All troubleshoot operations require a valid `network_id` resolved from `get_inventory`.
  - Never fabricate or guess `network_id`. If not resolved, do not invoke any troubleshoot operation.
- C2 Connectivity prerequisite:
  - `subscribe_speedtest` and `rpc_speedtest_serverlist` must not be invoked unless connectivity has been verified (ping check passed) or the user explicitly skips the check.
- C3 MAC guard:
  - All `subscribe_*` and `rpc_*` operations require `device_mac` resolved from `get_inventory`.
  - Never fabricate or guess `device_mac`. Always pass the exact MAC from the inventory device entry.
- C4 Required parameter guard:
  - For operations with required fields, never invent values:
    - `subscribe_ping` / `subscribe_traceroute` require `host`.
    - `rpc_poe_reset` requires `port_num`.
    - `rpc_ext_config_download` requires `name`, `url`, `checksum`, and `version`.
- C5 Port-stat reporting guard:
  - When `subscribe_port_stat` is invoked, the final response must include interpreted per-port link/counter findings and clearly call out abnormal ports.
  - Do not return raw payload only.
- C6 Download operation guard:
  - `download_packet_file` requires `interface`; `download_esg_eap_cert` requires `user_email`. Never invent these values.
  - `download_packet_file` is a PRO feature (gateway v1.2.45+); `download_esg_root_ca` and `download_esg_eap_cert` require gateway v1.2.85+ and v1.2.100+ respectively. Check device compatibility before invoking.
  - `download_*` operations return file content in `data.content`. Present the content to the user in a readable format where possible.
