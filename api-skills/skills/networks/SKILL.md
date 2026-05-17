---
name: networks
description: >
  Manage network settings. Use when the user wants to change general settings and Client Access Control settings  on a network.
---

## Persona & Output Rules — MANDATORY

⚠️ **Before responding to any user query that triggers this skill**, ensure `../../references/network-admin-persona.md` is loaded into your context:

- **If this is the first persona-aware skill called in this session**: use the **Read tool** to load it now, before any other action.
- **If you've already read persona.md earlier in this session**: you may rely on context (no need to re-read), but you MUST explicitly confirm to yourself which voice principles and escalation rules from persona.md apply to this query before responding.

The file defines voice principles, vocabulary translation (jargon → SMB-friendly), and the escalation matrix (when to reply with text vs dashboard vs action). Without applying it, the response won't match EnGenius brand voice for SMB customers — a product defect.

**Transparency rule**: if the user asks whether you read persona.md, answer honestly (e.g., "loaded earlier in this session, applied from context" vs "just loaded via Read tool").

# Network General Settings Plus Management

## Quick Reference

| Task | How |
|------|-----|
| Call any API operation | `python scripts/call_api.py --operation-id OPERATION_ID [--path-params 'JSON'] [--query-params 'JSON'] [--body 'JSON']` |
| Read API schema details | One file per operation: `references/<operation_id>.md` (file name equals the operation id). At plan-patch time, the runtime loads `references/<operation_id>.md` for the current `api_call` step. |

### Example

```bash
# GET — read current general policy plus
python scripts/call_api.py --operation-id get_general_policy_plus --path-params '{"orgId":"<orgId>","hvId":"<hvId>","networkId":"<networkId>"}'
```


## API Operations

### get_general_policy_plus

- method: GET
- path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/policy/general-settings-plus
- auth: x-auth-token header
- description: Fetch the full current general-settings-plus policy for baseline and post-update verification.

#### Path Parameters


| name      | type   | required | description                       |
| --------- | ------ | -------- | --------------------------------- |
| orgId     | string | true     | Target organization identifier.   |
| hvId      | string | true     | Target hierarchy view identifier. |
| networkId | string | true     | Target network identifier.        |


#### Query Parameters

(EMPTY)

#### Request Body

(EMPTY)

#### Response Body

> Full schema: [references/get_general_policy_plus.md](references/get_general_policy_plus.md).

### patch_general_policy_plus

- method: PATCH
- path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/policy/general-settings-plus
- auth: x-auth-token header
- description: Update one or more general-settings-plus fields using a schema-valid patch payload.

#### Path Parameters


| name      | type   | required | description                       |
| --------- | ------ | -------- | --------------------------------- |
| orgId     | string | true     | Target organization identifier.   |
| hvId      | string | true     | Target hierarchy view identifier. |
| networkId | string | true     | Target network identifier.        |


#### Query Parameters

(EMPTY)

#### Request Body

> Full schema: [references/patch_general_policy_plus.md](references/patch_general_policy_plus.md).

### get_user_profile

- method: GET
- path: /user/profile
- auth: x-auth-token header
- description: Return the user profile.

#### Path Parameters

(EMPTY)

#### Query Parameters

(EMPTY)

#### Response Body

> Full schema: [references/get_user_profile.md](references/get_user_profile.md).

### get_ssid_profiles

- method: GET
- path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/policy/aps/ssid-profiles
- auth: x-auth-token header
- description: Retrieve SSID profiles in the network. Use query param `constrain` when you need only profiles that meet a constraint (e.g. LAN port assignment: `constrain=usable_by_lan_ports`). Omit or use empty string for all profiles.

#### Path Parameters


| name      | type   | required | description                       |
| --------- | ------ | -------- | --------------------------------- |
| orgId     | string | true     | Target organization identifier.   |
| hvId      | string | true     | Target hierarchy view identifier. |
| networkId | string | true     | Target network identifier.        |


#### Query Parameters


| name              | type    | required | description                                                                                                              |
| ----------------- | ------- | -------- | ------------------------------------------------------------------------------------------------------------------------ |
| constrain         | string  | false    | Optional. `usable_by_lan_ports` — only SSID profiles assignable to LAN ports. Omit or use empty string for all profiles. |
| ssid_name         | string  | false    | Optional. Case-insensitive partial match on SSID name.                                                                   |
| is_emergency_wifi | boolean | false    | Optional. Filter by emergency WiFi flag.                                                                                 |


#### Response Body

> Full schema: [references/get_ssid_profiles.md](references/get_ssid_profiles.md).

### create_network_acls

- method: POST
- path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/acls
- auth: x-auth-token header
- description: Add a client to the Network/AP/Gateway ACL blocklist, allowlist, or VIP client list. MLD client creation is not supported.

#### Path Parameters


| name      | type   | required | description                       |
| --------- | ------ | -------- | --------------------------------- |
| orgId     | string | true     | Target organization identifier.   |
| hvId      | string | true     | Target hierarchy view identifier. |
| networkId | string | true     | Target network identifier.        |


#### Query Parameters

(EMPTY)

#### Request Body

> Full schema: [references/create_network_acls.md](references/create_network_acls.md).

#### Response Body

(EMPTY)

### get_network_acls

- method: GET
- path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/acls
- auth: x-auth-token header
- description: Return the ACL blocklist, allowlist, or VIP client list in the Network/AP/Gateway.

#### Path Parameters


| name      | type   | required | description                       |
| --------- | ------ | -------- | --------------------------------- |
| orgId     | string | true     | Target organization identifier.   |
| hvId      | string | true     | Target hierarchy view identifier. |
| networkId | string | true     | Target network identifier.        |


#### Query Parameters


| name        | type    | required | description                                         |
| ----------- | ------- | -------- | --------------------------------------------------- |
| access      | string  | true     | List type to return. Enum: `block`, `white`, `vip`. |
| from        | integer | false    | Pagination offset.                                  |
| count       | integer | false    | Pagination limit.                                   |
| order       | string  | false    | Sort order.                                         |
| search      | string  | false    | Search by `description` or `mac`.                   |
| sort        | string  | false    | Sort field. Enum: `mac`. Default: `mac`.            |
| device_type | string  | false    | Filter by device type. Enum: `ap`, `gateway`.       |


#### Request Body

(EMPTY)

#### Response Body

> Full schema: [references/get_network_acls.md](references/get_network_acls.md).

### delete_network_acls

- method: DELETE
- path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/acls
- auth: x-auth-token header
- description: Remove clients from the ACL blocklist, allowlist, or VIP client list in bulk.

#### Path Parameters


| name      | type   | required | description                       |
| --------- | ------ | -------- | --------------------------------- |
| orgId     | string | true     | Target organization identifier.   |
| hvId      | string | true     | Target hierarchy view identifier. |
| networkId | string | true     | Target network identifier.        |


#### Query Parameters

(EMPTY)

#### Request Body

> Full schema: [references/delete_network_acls.md](references/delete_network_acls.md).

#### Response Body

(EMPTY)

### patch_network_acls

- method: PATCH
- path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/acls/{clientMac}
- auth: x-auth-token header
- description: Update an ACL block/white/VIP client's description or scope in network, AP's SSID profile, or Gateway.

#### Path Parameters


| name      | type   | required | description                                                                   |
| --------- | ------ | -------- | ----------------------------------------------------------------------------- |
| orgId     | string | true     | Target organization identifier.                                               |
| hvId      | string | true     | Target hierarchy view identifier.                                             |
| networkId | string | true     | Target network identifier.                                                    |
| clientMac | string | true     | Target client MAC address. Use `mld_mac_addr` when `is_mld_client` is `true`. |


#### Query Parameters

(EMPTY)

#### Request Body

> Full schema: [references/patch_network_acls.md](references/patch_network_acls.md).

#### Response Body

(EMPTY)

## Flow Modules (Execution Order)

Use the following flow modules in order. Keep each module independent, so adding a new module does not change existing module behavior unless explicitly stated.

---

### F0. Prerequisite Gate and Flow Routing

**Purpose:** Resolve canonical ids so downstream APIs accept them (C1), then select the correct module sequence so no step is skipped or misapplied.

1. **Resolve identifiers** — missing `orgId`: load skill `orgs`, call `get_user_orgs`. Missing `networkId` or `hierarchy_view_id`: load skill `hvs`, call `get_hierarchy_views`.
2. **Select flow** — one operation type per run:


| Operation                                                                 | Flow                   |
| ------------------------------------------------------------------------- | ---------------------- |
| General settings — **includes country change**                            | F0 → F1 → F2 → F3 → F5 |
| General settings — **no country change** (e.g. time_zone, snmp, NTP, LED) | F0 → F2 → F3 → F5      |
| **Client Access Control** (ACL create/patch/delete)                       | F0 → F2 → F4 → F5      |


---

### F1. Country Compliance

**Purpose:** Collect legally required consent before changing network country. Without this record, the country change has no audit trail.

1. Call `get_user_profile`; extract `email`, `given_name`, `country`.
2. Load the reference document `references/change_country_terms_and_conditions.md`. Fill placeholders:
  - `current_network_country` ← profile `country`
  - `new_network_country` ← user intent
  - `requester_email` ← profile `email`
  - `date` ← current UTC ms
3. Present the filled document and stop to ask the user to clarify. Require **Requester Full Legal Name** and **Accept**; block until both are provided.
4. Store `compliance_record` (`legal_name`, `datetime`); pass to F3.

---

### F2. Preflight Validation and State Fetch

**Purpose:** Run preflight checks, then fetch current server state so the next mutation module (F3 or F4) builds requests from live data instead of assumptions. No mutation happens in F2.

Before state fetch, evaluate these checks:

- **Input validity check:** If required inputs are malformed (for example invalid MAC shape, invalid role-like ACL intent, missing required country target on country-change requests), stop and report the invalid input.
- **Idempotency check:** If the target state already equals the current state and no mutation is required, stop and report no change needed.
- **Missing context check:** If identifiers or selection context are still unresolved, stop and ask the user to clarify before planning mutation steps.

**For General settings (next is F3):**

- Call `get_general_policy_plus`; response populates Structured Memory `general_policy_snapshot_candidates` for F3 to reference.
- If change touches `lan_ports` or `lan_ports_by_model`: also call `get_ssid_profiles` with `constrain=usable_by_lan_ports`; build `ssid_name → id` lookup and pass to F3.

**For Client Access Control (next is F4):**

- **Create:** If user gave SSID names, call `get_ssid_profiles`; build `ssid_name → id` table and pass to F4.
- **Patch:** Call `get_network_acls` with the relevant `access` and `device_type`; build `field → value` table and pass to F4 as PATCH body base. If user gave SSID names, also call `get_ssid_profiles` and pass `ssid_name → id` table.
- **Delete:** Call `get_network_acls` only when the user did not fully specify targets (e.g. "remove the one we added"); pass list to F4 for building `clients`. Skip if user already gave exact mac/scope/device_type per client.

---

### F3. Schema-First Guard — General Settings Patch

**Purpose:** Build a schema-valid **partial** PATCH body from live state: include only the user-requested top-level fields so unrelated settings are not overwritten and the API accepts the call on the first attempt (C4).

**Inputs:** Structured Memory `general_policy_snapshot_candidates` (populated by F2's `get_general_policy_plus` call); optional `ssid_name → id` lookup from F2.

1. MUST load `references/patch_general_policy_plus.md` and `references/patch_rules.md` (C4 — must happen before any patch call).
2. Map user-described settings to exact schema field names in `references/patch_general_policy_plus.md` (e.g. "LED" → `is_ap_led_enable`, "時區" → `time_zone`). If any term cannot be confidently mapped, stop and ask the user to clarify before proceeding. Resolve SSID names via F2 lookup when LAN Port Settings are involved.
3. Build and audit PATCH body (C1/C2):
  a. **Identify changed top-level fields:** List which schema fields the user wants to modify (from the request schema in `references/patch_general_policy_plus.md`).
  b. **Value sourcing (never use illustrative examples in reference files as live values — C6):**
    - **Scalar** top-level fields (e.g. `time_zone`, `is_ap_led_enable`): use the value from the user request; validate shape against `references/patch_general_policy_plus.md`.
    - **Object** top-level fields (e.g. `custom_ntp_server`, `snmp_v3`, `ap_wifi_calling`): copy the **complete** object from `general_policy_snapshot_candidates[0]`, then overwrite only the user-requested sub-fields. The API does not support deep partial updates on objects — every sub-field required by validation must still be present. If the object is missing or empty in Structured Memory, re-fetch `get_general_policy_plus`; do not invent values.
    - **Arrays inside objects** (e.g. `providers` under `ap_wifi_calling`, `white_list` under `ap_malicious_url_filtering`): follow R1 in `patch_rules.md` — start from the full existing array in the snapshot or dedicated candidates, apply append / update / remove, then send the **full resulting array** in the PATCH body.
  c. **Assemble partial body:** Include **only** the top-level keys for fields the user is changing. **Do not** include unrelated top-level keys. **Do not** send a full copy of the entire GET response as the PATCH body.
  d. **Rule-check table:** Evaluate every rule and record the result:

  | Rule ID | Category             | Applies? | Action |
  | ------- | -------------------- | -------- | ------ |
  | R1      | Array mutations      | Yes / No | ...    |
  | R2      | Field exclusion      | Yes / No | ...    |
  | R3      | Country / compliance | Yes / No | ...    |
  | R4      | Custom NTP gate      | Yes / No | ...    |
  | R5      | WiFi Calling gate    | Yes / No | ...    |
  | R6      | LAN Port settings    | Yes / No | ...    |

  e. Finalize PATCH body only after the table is complete.
4. Validate payload against the `patch_general_policy_plus` request schema in `references/patch_general_policy_plus.md`.
5. Invoke `patch_general_policy_plus`.

---

### F4. Schema-First Guard — Client Access Control

**Purpose:** Build a schema-valid ACL request from F2 state so identifiers (mac, scope, ssid_profile_ids) are correct and the API accepts it on the first call (C4).

**Inputs from F2 (as applicable):** get_network_acls response; `ssid_name → id` lookup.

1. MUST load the applicable per-operation reference(s) under `references/` for each ACL call in this run — e.g. `create_network_acls.md`, `get_network_acls.md`, `patch_network_acls.md`, or `delete_network_acls.md` (C4 — must happen before any ACL API call).
2. Map user-described ACL intent to exact schema field names in those files (e.g. "黑名單" → `access: "block"`, "白名單" → `access: "white"`, "VIP" → `access: "vip"`). Extract list type, target client(s), and operation-specific params. If any term cannot be confidently mapped, stop and ask the user to clarify. Resolve SSID names and clientMac/from_device_type/scope from F2 state.
3. **Create** — Classify user intent into one of three scope variants before building body:
  - **Wireless → All SSIDs** (user says "all SSIDs" / "整個網路"): `device_type: "ap"`, `scope: "network"`, omit `ssid_profile_ids`.
  - **Wireless → specific SSID(s)** (user names SSID(s)): `device_type: "ap"`, `scope: "ssid"`, `ssid_profile_ids` (≥1, resolve names via F2 lookup).
  - **Gateway** (user says "gateway" / "LAN"): `device_type: "gateway"`, omit `scope` and `ssid_profile_ids`.
  - If the user says "block on wireless" without specifying All SSIDs vs specific SSID(s), stop and ask the user to clarify before proceeding.
   Build body for `create_network_acls` with required `mac`, `access` plus the fields from the matched variant. Validate; invoke `create_network_acls`.
4. **Patch** — `patch_network_acls` body schema differs from Create: no `mac`, no `device_type`; uses `from_device_type` + `to_device_type` instead. See `references/patch_network_acls.md` for full field definitions.

  **Path param:**

  | param | source |
  |---|---|
  | clientMac | Structured Memory `network_acl_candidates` → matched client `mac` (MLD: use `mld_mac_addr`) |

  **Body field sources (C5):**

  | field | required | source | notes |
  |---|---|---|---|
  | access | yes | user intent | `block` / `white` / `vip` |
  | from_device_type | yes | **Structured Memory `network_acl_candidates`** | Copy `device_type` of matched client **verbatim**. NEVER from user intent. |
  | to_device_type | yes | user intent | See scope variant table below |
  | scope | conditional | user intent | Only when `to_device_type` = `ap` |
  | ssid_profile_ids | conditional | Structured Memory `ssid_profile_candidates` | Only when `scope` = `ssid` (≥1 item) |
  | description | optional | user intent | |
  | is_mld_client | conditional | Structured Memory `network_acl_candidates` | `true` when `clientMac` is MLD MAC |

  **Scope variants (determine `to_device_type` only — never affects `from_device_type`):**

  | user intent | to_device_type | scope | ssid_profile_ids |
  |---|---|---|---|
  | Wireless → All SSIDs ("整個網路") | `ap` | `network` | omit |
  | Wireless → specific SSID(s) | `ap` | `ssid` | ≥1, resolve via Structured Memory |
  | Gateway / LAN | `gateway` | omit | omit |

  Validate body; invoke `patch_network_acls`.
5. **Delete** — Build body for `delete_network_acls`: required `access`, `clients` (each: `mac`, `device_type`; for AP add `scope`; for MLD set `is_mld_client`, use `mld_mac_addr` as `mac`). Derive from F2 ACL list when user did not specify exact clients. Validate; invoke `delete_network_acls`.

---

### F5. Post-Update Verification

**Purpose:** Verify the mutation actually took effect so the agent never reports success on a silently failed change.

1. **After F3:** Invoke `get_general_policy_plus`; response updates Structured Memory `general_policy_snapshot_candidates`. Compare each requested field against `general_policy_snapshot_candidates[0]`. On mismatch, stop and respond to the user with failure details.
2. **After F4:** Invoke `get_network_acls` with the same `access` (and `device_type`) used in F4. Confirm expected state (created client present / patched fields updated / deleted client absent). On mismatch, stop and respond to the user with failure details.
3. All checks pass, stop and respond to the user with confirmed updated fields.

---

### F6. API Naming and Reference Rule

1. When invoking an API operation, use only the plain `operation_id` as defined in the `## API Operations` section above.
2. If response schema detail is unclear, read `references/<operation_id>.md` for that operation.

## Constraints (Hard Rules)

These constraints apply across all flow modules. Append new constraints as new C* items without rewriting existing ones.

- **C1 Identifier and PATCH base**
  - `orgId`, `hvId`, `networkId` must be canonical ids resolved via GETs (e.g. `get_user_orgs`, `get_hierarchy_views`). Never pass user-facing names or aliases as path parameters; never guess identifiers.
  - PATCH payload must include **only** the top-level fields the user wants to modify. Do not include unrelated top-level fields. For object fields, read the complete object from Structured Memory `general_policy_snapshot_candidates` and overwrite only the user-requested sub-fields. PATCH body must not be empty when performing an update.
  - If violated: do not proceed with mutation; stop and report the reason to the user.
- **C2 Schema field mapping**
  - Map user-requested changes to the exact field names and nested structure in `references/<operation_id>.md` for the operation being invoked. Use only names and shapes defined in the schema (e.g. `custom_ntp_server`, not `enableCustomNtpServer`). Request body must be valid JSON.
  - If violated: do not proceed with mutation; stop and report schema mismatch to the user.
- **C3 Operation naming and reference**
  - Invoke API operations using only the plain `operation_id`; do not use `skill_name.operation_id`.
  - If schema detail is unclear, read `references/<operation_id>.md` for that operation.
  - If violated: do not proceed; fix operation naming/reference context first.
- **C4 Schema-first (no failure-driven retry)**
  - Load schema (and for general-settings patch, `patch_rules.md`) before the first mutation API call. Do not call a mutation API first, receive 4xx, then load schema and retry. Applies to general-settings PATCH and to ACL create/patch/delete.
  - If violated: do not proceed with mutation; load references first.
- **C5 ACL Patch `from_device_type` derivation**
  - `from_device_type` in `patch_network_acls` body MUST equal the `device_type` value from the matched client entry in Structured Memory `network_acl_candidates` (originally populated by `get_network_acls`). Look up `network_acl_candidates` by `mac`, read its `device_type`, and copy that value verbatim as `from_device_type`. Never assume, guess, or copy from user intent or from `to_device_type`. Example: if `network_acl_candidates` shows `{"mac": "c6:66:f6:1f:f7:14", "device_type": "gateway"}` and user wants to move to AP → `from_device_type: "gateway"`, `to_device_type: "ap"`.
  - If violated: do not proceed with `patch_network_acls`; report invalid source derivation to the user.
- **C6 No example-value substitution**
  - When assembling any request body, field values MUST come from Structured Memory or user input. If a required value cannot be found in Structured Memory, stop and ask the user to clarify. NEVER substitute values from illustrative examples in `references/<operation_id>.md` — they are fictional and may silently corrupt live data.
  - If violated: do not proceed with mutation; request missing live value context.
