---
name: org-devices
description: >
  Organization device inventory mutation: list inventory, get expired info, register serials,
  rename/undo license on device, assign/remove from networks, de-register,
  cross-org device moves, RMA replacement. Use this skill to fetch deviceId, serial number and device mac
  before calling org-license, network-ap-troubleshoot, network-gateway-troubleshoot and network-switch-troubleshoot skills.

---

## Persona & Output Rules — MANDATORY

⚠️ **Before responding to any user query that triggers this skill**, ensure `../../references/network-admin-persona.md` is loaded into your context:

- **If this is the first persona-aware skill called in this session**: use the **Read tool** to load it now, before any other action.
- **If you've already read persona.md earlier in this session**: you may rely on context (no need to re-read), but you MUST explicitly confirm to yourself which voice principles and escalation rules from persona.md apply to this query before responding.

The file defines voice principles, vocabulary translation (jargon → SMB-friendly), and the escalation matrix (when to reply with text vs dashboard vs action). Without applying it, the response won't match EnGenius brand voice for SMB customers — a product defect.

**Transparency rule**: if the user asks whether you read persona.md, answer honestly (e.g., "loaded earlier in this session, applied from context" vs "just loaded via Read tool").

# Organization Devices and Inventory

Use this skill for **device-centric** Cloud inventory and network attachment. For **org membership** use **team-members**. For **org-wide license list/tab** without device ops, use **licenses**. Use **orgs** only to resolve **`orgId`** when unknown.

## Quick Reference

| Task | How |
|------|-----|
| Call any API operation | `python scripts/call_api.py --operation-id OPERATION_ID [--path-params 'JSON'] [--query-params 'JSON'] [--body 'JSON']` |
| Read API schema details | Read `references/<operation_id>.md` |

### Example

```bash
python scripts/call_api.py --operation-id get_inventory --path-params '{"orgId":"<orgId>"}'
```

## API Operations

For each operation below, full request/response schema details are in `references/<operation_id>.md`.

### get_inventory
- method: GET
- path: /orgs/{orgId}/inventory
- auth: x-auth-token header
- description: Return a list of devices from the org inventory.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

| name | type   | required | default | description |
| ---- | ------ | -------- | ------- | ----------- |
| from | integer | false | 0 | Index of the list started (pagination). |
| count | integer | false | 10 | Number of items to return. |
| order | string | false | + | Sort order: literal character `+` (ascending) or `-` (descending). Pass `+` or `-` only; do not pass `'+'` or `'-'` (quoted). |
| sort | string | false | type | Sort field. See `references/get_inventory.md` for enum details. |
| type | string | false | none | Filter by device type (ap, switch, ezmaster, bsc, gateway, pdu, switch_extender, camera, nvs). |
| series | string | false | none | Filter by series (Cloud, Cloud-Lite). |
| usage | string | false | none | Filter: used or unused. |
| usable_license_type | string | false | none | Filter devices by license type (pro, pro-v, pro-r, pro-lite, unlimited). |
| search | string | false | none | Regex pattern. Search in name, mac, model, network_name, serial_number, etc. Use `(?i)(keyword)` for case-insensitive match (e.g. search for "ECW260" → `(?i)(ECW260)`). |
| is_expired | boolean | false | none | Filter by expiration. |

#### Request Body

(EMPTY)

### register_inventory
- method: POST
- path: /orgs/{orgId}/inventory
- auth: x-auth-token header
- description: Register devices to the org inventory by serial number. Use when the user wants to register device(s) onto EnGenius Cloud inventory. Request body is a JSON array of objects, each with required `serial_number` (one per device). Response is an array of per-device results (code, message, status: ok, invalid, unexisting, used, error).

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body

Body is a JSON array of objects; each object has required field `serial_number`. Example: `[ {"serial_number": "1650QCHPJ6C2"}, {"serial_number": "1711QC11M1"} ]`. Do not use a flat key-value; pass the array as the request body.

### patch_inventory
- method: PATCH
- path: /orgs/{orgId}/inventory/{deviceId}
- auth: x-auth-token header
- description: Update a device: **(1) name/description** — body `action: patch_device_info`, optional `name`, optional `description`; **(2) undo license** — body `action: undo_license` (only within 7-day grace period, disassociates license from device). **You must call get_inventory first** to get the device's `id`; then call patch_inventory with that `id` as path_param deviceId. Do NOT use serial_number or mac — only the `id` from get_inventory response (24-char hex).

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |
| deviceId | string | true     | The device's **id** from get_inventory response (`devices[].id`). Obtain it in Step 1 below; never use serial_number or mac. |

#### Query Parameters

(EMPTY)

#### Request Body

Body is a JSON object. **Cases:** (1) `action: patch_device_info` — optional `name`, `description`; send only fields to change. (2) `action: undo_license` — body must be **only** `{ "action": "undo_license" }`; do NOT add `confirmation` or other keys (API does not accept them). Valid only within 7-day grace period. Examples: `{ "action": "patch_device_info", "name": "Device 01" }`; `{ "action": "undo_license" }`.

### add_device
- method: POST
- path: /orgs/{orgId}/hvs/{hvId}/networks/{networkId}/devices
- auth: x-auth-token header
- description: Assign one or more devices from org inventory to a network. Use when the user wants to assign device(s) to a network (UI: Device page → select device(s) → Assign to Network). Requires resolved orgId, hvId, and networkId (e.g. from get_user_orgs + get_hierarchy_views). Request body is a JSON array of objects with device id.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |
| hvId | string | true     | Hierarchy view identifier (from get_hierarchy_views). |
| networkId | string | true     | Target network identifier (from hierarchy view networks). |

#### Query Parameters

(EMPTY)

#### Request Body

Body is a JSON array of objects; each object has required `id` (device id from org inventory). Optional: `is_config_overwrite_pending` (boolean), `is_gateway_ha_backup_unit_added` (boolean, default false). Example: `[ {"id": "<device_id_1>"}, {"id": "<device_id_2>"} ]`.

### delete_devices
- method: DELETE
- path: /orgs/{orgId}/devices
- auth: x-auth-token header
- description: Remove one or more devices from their networks (bulk delete). Use when the user wants to remove device(s) from a network (UI: Device page → select device(s) → Remove from Network). Requires resolved orgId. Request body is a JSON array of objects with device_id and network_id (the network from which to remove each device).

**Pure deletion:** When this call is the **user’s explicit intent** to remove device(s) from a network (not an internal step inside de-register Flow 9 or move-device C11), do **not** call this API unless the user has explicitly confirmed (e.g. "Yes") in the **immediately preceding** turn. If confirmation is missing, stop and ask: "Are you sure you want to remove the selected device(s) from their network(s)?" Do not call any API until confirmed. Only after confirmation, call `delete_devices`.

**Flow 9 (de-register):** When `delete_devices` is used **only** as the prerequisite before `deregister_org_device` for the **same** de-register request, it is covered by the **single** de-register confirmation — do **not** prompt separately for “remove from network” and then again for “de-register.”

**Turn boundary:** You may call read-only APIs in the same turn (e.g. `get_user_orgs`, `get_inventory`) to resolve org, device id, and network. If confirmation is still missing after that, your user-facing output for that turn must be **only** the confirmation question (optionally with a brief recap: friendly device name/serial, org, network). **Do not** call `delete_devices` in that same turn. **Do not** imply the removal already happened. Treat the user’s **next** message as answering your question; only then may you perform the DELETE.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body

Body is a JSON array of objects; each object has required `device_id` and `network_id` (the network from which to remove the device). Get device id and current network_id from org inventory (`get_inventory`). Example: `[ {"device_id": "<id>", "network_id": "<network_id>"}, ... ]`.

### deregister_org_device
- method: DELETE
- path: /orgs/{orgId}/inventory/{deviceId}
- auth: x-auth-token header
- description: De-register a device from the org inventory (remove from EnGenius Cloud). Use when the user wants to remove registered device(s) from Cloud inventory (UI: Device page → select device(s) → De-Register Device). Requires resolved orgId and deviceId. For multiple devices, call once per device. **Before the first `delete_devices` or `deregister_org_device` call for this user intent**, ask the user **once** to confirm de-registration, and wait for their explicit agreement in a **later** turn when possible; only then call the DELETE APIs (see Flow 9 and C12). That **one** confirmation authorizes **both** `delete_devices` (when the device is still on a network) and `deregister_org_device` in sequence — **no second confirmation** between them.

**Pure deletion:** Same spirit as team-members F7 (membership deletion): do **not** proceed with `deregister_org_device` (or the paired `delete_devices` in Flow 9) unless the user has explicitly confirmed de-registration—ideally with "Yes" in the **immediately preceding** turn when the flow allows. If confirmation is missing, stop and ask using friendly device name/serial; do not call any DELETE API. Only after that **single** confirmation, run Flow 9: `delete_devices` if still on a network, then `deregister_org_device` per device **without asking again in between**.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |
| deviceId | string | true     | Device identifier (from org inventory). |

#### Query Parameters

(EMPTY)

#### Request Body

(EMPTY)

### move_devices_between_orgs
- method: POST
- path: /orgs/{orgId}/inventory/move
- auth: x-auth-token header
- description: Move devices from the current org (path orgId) to a target org (body org_id). Use when the user wants to **move device(s) to another organization** (Change Organization; Device page → move device to other org).

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | **Source** organization identifier (current org of the devices). |

#### Query Parameters

(EMPTY)

#### Request Body

Body is a JSON object. Required: `org_id` (string) — **target** organization identifier (24-char hex). Required: `device_ids` (array of strings) — device id(s) from source org inventory. Example: `{ "org_id": "5d3a70dfae4a1400010a36d7", "device_ids": ["5cd28b893550730001fa48zz", "..."] }`. Resolve device ids from `get_inventory` with source orgId; resolve target org_id from `get_user_orgs` (user must have access to target org).

### create_device_replacement
- method: POST
- path: /orgs/{orgId}/inventory/{deviceId}/replacement
- auth: x-auth-token header
- description: Replace the specific device by another device of the same model from the org inventory (RMA/DoA). The replaced device’s license is transferred to the new device and the old device’s license expires. **Path deviceId** = the device to be replaced (old). **Body device_id** = the replacement device (new) from inventory. **Body mode** is required: `replace` (replaced device **moved to Inventory**) or `replace_and_deregister` (replaced device de-registered from org for RMA). When the user wants the old device to go to Inventory, use **mode=replace** — do NOT say this API cannot move a device to inventory. If the user does not clearly specify which mode, ask a direct follow-up question (e.g. "Replace (old device to inventory) or Replace and de-register for RMA?"). See `references/create_device_replacement.md` for mode (UI) table.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |
| deviceId | string | true     | The **replaced** device’s id (device to be replaced; from get_inventory). Do NOT use serial_number or mac. |

#### Query Parameters

(EMPTY)

#### Request Body

Required. JSON object: `device_id` (string) — the **replacement** device’s id from get_inventory (same model); `mode` (string) — `replace` or `replace_and_deregister`. Example: `{ "device_id": "6108fe9382bcdd7d877ad896", "mode": "replace" }`.

### get_expired_devices_info
- method: GET
- path: /orgs/{orgId}/expired-devices-info
- auth: x-auth-token header
- description: Returns license-expiry summary for the org. Use when the user asks about **earliest expired date** (remind users to add license by then), **expired devices count** (e.g. AP in "Pro" license mode cannot be managed by Cloud and show off-line in Network), or **expire within 30 days** count. Cloud sends notifications when devices will expire within 30 days and within 3 days. Response: `earliest_expired_date` (ms or null), `expired_devices_count`, `expired_devices_count_in_30_days`.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body

(EMPTY)

## Flow Modules (Execution Order)

Use the following flow modules in order.

### F1. Prerequisite Gate (Identifier Resolution)

1. If **`orgId`** is missing or not trusted in context: load skill **`orgs`**, call **`get_user_orgs`**, resolve canonical **`orgId`**. Never pass org **names** as ids.
2. If the task needs **`hvId`** / **`networkId`** / **`hierarchy_view_id`** (assign device, move between networks, create backup, apply template `network_ids`, etc.): load **`hvs`**, call **`get_hierarchy_views`** with resolved **`orgId`**.
3. Multi-org: if **`get_user_orgs`** returns multiple orgs and the user did not specify target org, stop and ask which org.


### F2. Inventory and reads

1. Device list/search: call **`get_inventory`** with **`orgId`**. **`search`** query uses regex — for keywords use `(?i)(keyword)`. **`order`** must be exactly **`+`** or **`-`** (one character).
2. License expiry summary: call **`get_expired_devices_info`** with **`orgId`** when the user asks for earliest expiry date, expired device counts, or expire-within-30-days counts.

### F3. Register / patch device info / undo license

Register devices by serial number, rename/update metadata, or undo license during grace period.

1. Registration: **`register_inventory`** with body JSON array of `{ "serial_number": "..." }` per item.
2. Rename / description: **`get_inventory`** then **`patch_inventory`** with **`patch_device_info`**.
3. Undo license (grace period): **`get_inventory`** then **`patch_inventory`** body exactly `{ "action": "undo_license" }`.

### F4. Assign / remove / move networks / cross-org move / RMA

1. Assign to network: resolve **`hvId`**/**`networkId`** via **`get_hierarchy_views`**; resolve device ids via **`get_inventory`**; **`add_device`**.
2. Remove from network (user intent): **`delete_devices`** — respect **Pure deletion** unless part of Flow 4 or move pipeline.
3. De-register: **`get_inventory`** → ask once → if **`network_id`** set, **`delete_devices`** then **`deregister_org_device`** per device — one confirmation covers both deletes.
4. Move to another network: **`get_inventory`** → if **`network_id`** present **`delete_devices`** → **`get_hierarchy_views`** → **`add_device`**.
5. Move devices to another org: **`move_devices_between_orgs`** — source **`orgId`**, target **`org_id`** from **`get_user_orgs`**, **`device_ids`** from **`get_inventory`**.
6. Replacement (RMA): **`get_inventory`** for old and new device ids — **`create_device_replacement`** with **`mode`** clarified if needed.

### F5. API Naming and Reference Rule

1. Use plain `operation_id`: `get_inventory`, `register_inventory`, `patch_inventory`, `add_device`, `delete_devices`, `deregister_org_device`, `move_devices_between_orgs`, `create_device_replacement`, `get_expired_devices_info`. Do NOT prefix with skill name.
2. If response schema detail is unclear, load `references/<operation_id>.md`.


### F6. Pure Deletion Paths (Destructive DELETE APIs)

1. **Applies to:** `delete_devices` (remove-from-network intent), `deregister_org_device`. **`delete_devices`** as prerequisite for Flow 4 or move-device (**C10**) follows that parent confirmation—no second prompt for that internal step.
2. When the user explicitly asks to remove, delete, or de-register: do not call destructive DELETE until they have clearly confirmed (preferably "Yes" in the immediately preceding turn). If confirmation is missing, stop and ask per each operation’s **Pure deletion** paragraph.
3. **Multi-turn:** Do not summarize success as done while only asking confirmation.


## Constraints (Hard Rules)

- C1 Canonical org identifier: Never guess **`orgId`** — resolve via **`orgs`** **`get_user_orgs`** API data.
- C2 Operation naming: **`operation_id`** plain names only (`get_inventory`, `register_inventory`, `patch_inventory`, `add_device`, `delete_devices`, `deregister_org_device`, `move_devices_between_orgs`, `create_device_replacement`, `get_expired_devices_info`).
- C3 Output scope: Concise inventory answers; omit empty fields.
- C4 (subset): **`orgId`** canonical hex. Device path params use **`deviceId`** from **`get_inventory`** (`devices[].id`).
- C5 **`get_inventory`** **`search`** regex: `(?i)(keyword)` when user gives plain keyword.
- C6 Response field semantics: Match user question to correct response fields.
- C7 Do not expose internal IDs unless user asks.
- C8 **`add_device`**: **`hvId`**/**`networkId`** from **`get_hierarchy_views`**; device **`id`** from **`get_inventory`**.
- C9 **`delete_devices`**: **`device_id`**/**`network_id`** from **`get_inventory`**.
- C10 Move device: **`get_inventory`** → **`delete_devices`** if **`network_id`** → **`get_hierarchy_views`** → **`add_device`** — never **`add_device`** alone when **`network_id`** present.
- C11 De-register: confirm once → **`delete_devices`** if on network → **`deregister_org_device`**.
- C12 **`patch_inventory`**: Always **`get_inventory`** first for **`deviceId`**.
- C13 Time presentation (when showing times from inventory): use org **`time_zone`** from **`get_user_orgs`** for the resolved **`orgId`**.
- C14 **`move_devices_between_orgs`**: source path **`orgId`**, body **`org_id`** target; **`device_ids`** from **`get_inventory`**.
- C15/C16 **`create_device_replacement`**: path **`deviceId`** = old; body **`device_id`** = replacement; **`mode`** `replace` vs `replace_and_deregister`; never use org id as device id.
