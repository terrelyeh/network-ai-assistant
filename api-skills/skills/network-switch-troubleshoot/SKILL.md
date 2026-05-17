---
name: network-switch-troubleshoot
description: >
  Troubleshoot switch network devices. Use when the user wants real-time switch status,
  connectivity diagnostics (ping, traceroute), and Layer2 inspection (ARP/FDB/cable/port stats).
---

## Persona & Output Rules — MANDATORY

⚠️ **Before responding to any user query that triggers this skill**, ensure `../../references/network-admin-persona.md` is loaded into your context:

- **If this is the first persona-aware skill called in this session**: use the **Read tool** to load it now, before any other action.
- **If you've already read persona.md earlier in this session**: you may rely on context (no need to re-read), but you MUST explicitly confirm to yourself which voice principles and escalation rules from persona.md apply to this query before responding.

The file defines voice principles, vocabulary translation (jargon → SMB-friendly), and the escalation matrix (when to reply with text vs dashboard vs action). Without applying it, the response won't match EnGenius brand voice for SMB customers — a product defect.

**Transparency rule**: if the user asks whether you read persona.md, answer honestly (e.g., "loaded earlier in this session, applied from context" vs "just loaded via Read tool").

# Switch Network Troubleshoot

## API Operations

### subscribe_stat
- description: Subscribe to real-time switch device statistics

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_stat.md`.

### subscribe_ping
- description: Subscribe to real-time ping results for a target host

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_ping.md`.

### subscribe_traceroute
- description: Subscribe to real-time traceroute results for a target host

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_traceroute.md`.

### subscribe_arp_list
- description: Subscribe to real-time ARP table entries

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_arp_list.md`.

### subscribe_fdb_list
- description: Subscribe to real-time forwarding database entries

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_fdb_list.md`.

### subscribe_cable_diag
- description: Subscribe to real-time cable diagnostics for selected ports

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_cable_diag.md`.

### subscribe_port_stat
- description: Subscribe to real-time switch port statistics

#### Request Body

> Full request body schema and example: see API schema `references/subscribe_port_stat.md`.

## Flow Modules (Execution Order)

Use the following flow modules in order. Keep each module independent, so adding a new module does not change existing module behavior unless explicitly stated.

### F0. Prerequisite Gate (Identifier Resolution)

1. If required ids are missing, resolve in this order:
   - Load skill `orgs`, then invoke `get_user_orgs` to resolve canonical `orgId`.
   - Invoke `get_inventory` with resolved `orgId` to discover devices and their `network_id`, `mac`, and `network_name`.
   - Use user-provided names only as lookup hints; never fabricate IDs.
2. From the inventory response, identify the target switch device and resolve both its `network_id` and `mac`.
3. Pass `device_mac` (the resolved MAC address) as a required parameter to every `subscribe_*` operation.

### F1. Connectivity Check

1. After F0 passes and `network_id` is resolved, invoke `subscribe_ping` with `host: "8.8.8.8"` to verify the switch network has external connectivity.
2. If ping fails or returns no data, stop and report to the user that the network cannot reach the target host.

### F2. Core Diagnostics

1. For device health requests, invoke `subscribe_stat`.
2. For path analysis requests, invoke `subscribe_traceroute`.
3. For Layer2 table requests, invoke `subscribe_arp_list` and/or `subscribe_fdb_list` as needed.
4. For physical link troubleshooting, invoke `subscribe_cable_diag`.
5. For traffic counters and CRC visibility, invoke `subscribe_port_stat`.
6. When `subscribe_port_stat` is used, present a concise per-port summary including:
   - port/interface identifier
   - link state (`up`/`down`)
   - RX/TX throughput
   - RX/TX packet or error counters (especially CRC-related fields when available)
   - top abnormal ports with a short reason
   If data is empty or required counters are missing, explicitly report "no sufficient port statistics data" and provide a next diagnostic action.

### F3. Completion Convergence

1. Stop and respond to the user with:
   - What operation(s) were executed
   - Key findings from each operation response
   - Any failure points and next troubleshooting action

### F4. API Naming and Reference Rule

1. When invoking an API operation, use only the plain `operation_id` as defined in the `## API Operations` section above.
2. If request or response schema detail is unclear, load the reference schema from `references/<operation_id>.md`.

## Constraints (Hard Rules)

These constraints are independent from flow modules. New constraints should be appended as new `C*` items without rewriting existing ones.

- C1 Network ID guard:
  - All troubleshoot operations require a valid `network_id` resolved from `get_inventory`.
  - Never fabricate or guess `network_id`. If not resolved, do not invoke any troubleshoot operation.
- C2 Operation family guard:
  - Switch troubleshoot flow supports `subscribe_*` operations only. Do not plan or invoke other operation families.
- C3 Required parameter guard:
  - For operations with required fields, never invent values:
    - `subscribe_ping` / `subscribe_traceroute` require `host`.
    - `subscribe_arp_list` / `subscribe_fdb_list` require `page_size`.
    - `subscribe_cable_diag` requires `ports`.
- C4 MAC guard:
  - All `subscribe_*` operations require `device_mac` resolved from `get_inventory`.
  - Never fabricate or guess `device_mac`. Always pass the exact MAC from the inventory device entry.
- C5 Port-stat reporting guard:
  - When `subscribe_port_stat` is invoked, the final response must include interpreted per-port link/counter findings and clearly call out abnormal ports.
  - Do not return raw payload only.
