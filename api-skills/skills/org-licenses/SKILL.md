---
name: org-licenses
description: >
  Organization license pool: list licenses, add license key, assign to device,
  auto-associate key units, batch association, move inactive unassociated licenses
  between orgs.
---

## Persona & Output Rules — MANDATORY

⚠️ **Before responding to any user query that triggers this skill**, ensure `../../references/network-admin-persona.md` is loaded into your context:

- **If this is the first persona-aware skill called in this session**: use the **Read tool** to load it now, before any other action.
- **If you've already read persona.md earlier in this session**: you may rely on context (no need to re-read), but you MUST explicitly confirm to yourself which voice principles and escalation rules from persona.md apply to this query before responding.

The file defines voice principles, vocabulary translation (jargon → SMB-friendly), and the escalation matrix (when to reply with text vs dashboard vs action). Without applying it, the response won't match EnGenius brand voice for SMB customers — a product defect.

**Transparency rule**: if the user asks whether you read persona.md, answer honestly (e.g., "loaded earlier in this session, applied from context" vs "just loaded via Read tool").

# Organization Licenses

Use this skill for **License tab** and license pool operations. Use **devices** for **`get_inventory`** when association flows need device ids. Use **orgs** only to resolve **`orgId`**.

## Quick Reference

| Task | How |
|------|-----|
| Call any API operation | `python scripts/call_api.py --operation-id OPERATION_ID [--path-params 'JSON'] [--query-params 'JSON'] [--body 'JSON']` |
| Read API schema details | Read `references/<operation_id>.md` |

### Example

```bash
python scripts/call_api.py --operation-id get_licenses --path-params '{"orgId":"<orgId>"}'
```

## API Operations

For each operation below, full request/response schema details are in `references/<operation_id>.md`.

### get_licenses
- method: GET
- path: /orgs/{orgId}/licenses
- auth: x-auth-token header
- description: Return a list of licenses under the org. Use when the user asks about org licenses, license list, or license tab (UI: Organization > Inventory & License > License tab). **When `license_type=pro_license` (Per-Device licensing)**: The Per-Device model assigns a license directly to a specific device. There are two feature plans — BASIC and PRO. You need an AP Pro license to use AP Pro features, and a Switch license for Switch. Details: https://www.engenius.ai/cloud/licenses. Filter by `license_type=pro_license` to list Per-Device (PRO) licenses; use `license_category` (ap, switch, gateway, pdu, switch_extender, epc, camera, ai) to narrow by device type.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

| name | type   | required | default | description |
| ---- | ------ | -------- | ------- | ----------- |
| from | integer | false | 0 | Pagination start index. |
| count | integer | false | 10 | Number of items to return. |
| order | string | false | + | Sort order: `+` (asc) or `-` (desc). Pass `+` or `-` only; do not pass quoted. |
| sort | string | false | activated_date | Sort field: license_type, license_key, duration, issued_date, activated_date, time_remaining, status, associated_device, license_key_model, added_by. |
| license_category | string | false | none | Filter by category: ap, switch, gateway, pdu, switch_extender, epc, camera, ai. |
| license_type | string | false | none | Filter by type: pro, pro-v, pro-r, pro-lite, connect, backup, secupoint, **pro_license** (Per-Device PRO), epc_license, ai_license. |
| is_co_terminated | boolean | false | none | Filter Co-Term licenses. |
| is_epc_device_only | boolean | false | none | Filter EPC device-only licenses. |
| status | string | false | none | Filter by status: inactive, active, merging, merged, expired, canceled. |

#### Request Body

(EMPTY)

### get_license_key
- method: GET
- path: /license-keys/{licenseKey}
- auth: x-auth-token header
- description: Return metadata for a license key (no `orgId` needed). Use to preview a license key before binding it to an org. Add flow should be: `get_license_key` → show summary to user → explicit confirmation → `add_license_key`.

#### Path Parameters

| name | type | required | description |
| ---- | ---- | -------- | ----------- |
| licenseKey | string | true | License key string (for example `AAAAAA-BBBBBB-CCCCCC-DDDDDD`). |

#### Query Parameters

(EMPTY)

#### Request Body

(EMPTY)

### add_license_key
- method: POST
- path: /orgs/{orgId}/license-keys/{licenseKey}
- auth: x-auth-token header
- description: Add a license key to an organization (UI: Organization > Inventory & License > License → Add License). After add, the key extends to multiple license units (same issued_date). Optional: user can later use Auto Associate to bind units to devices without license.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |
| licenseKey | string | true     | The license key string to add.  |

#### Query Parameters

(EMPTY)

#### Request Body

Optional. If the API accepts it, body may include added_by (string, e.g. user email). Otherwise send empty object {}.

### assign_license
- method: POST
- path: /orgs/{orgId}/inventory/{deviceId}/licenses
- auth: x-auth-token header
- description: **Associate to Device** — Auto associate a license to a device in the org. Use when the user wants to assign an existing (unassociated or available) license to a specific device. Resolve deviceId from get_inventory (`devices[].id`); do NOT use serial_number or mac. Request body: required `days` (integer, e.g. 365), optional `license_type` (pro, pro-r, pro-v, pro-lite, secupoint, unlimited; omit or null = pro).
#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier (24-char hex). |
| deviceId | string | true     | Device id from get_inventory (`devices[].id`). Do NOT use serial_number or mac. |

#### Query Parameters

(EMPTY)

#### Request Body

Required. JSON object: `days` (integer, required), `license_type` (string, optional; pro, pro-r, pro-v, pro-lite, secupoint, unlimited; null = pro). Example: `{ "days": 365, "license_type": "pro" }`.

### auto_associated_license_key
- method: POST
- path: /orgs/{orgId}/license-keys/{licenseKey}/auto-association
- auth: x-auth-token header
- description: **Associate to Device (Auto Associate)** — Auto associate the license key's units to the given devices. Same behavior as clicking "auto associate" when you add a license (License → Add License → Auto Associate). Use only when doing that add-then-auto-associate flow. **device_ids must be device id (24-char hex from get_inventory `devices[].id`), never MAC address or serial_number.** Resolve orgId, licenseKey, and device_ids from get_inventory.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier (24-char hex). |
| licenseKey | string | true     | The license key string (e.g. AAAAAA-BBBBBB-CCCCCC-DDDDDD) already added to the org. |

#### Query Parameters

(EMPTY)

#### Request Body

Required. JSON object: `device_ids` (array of strings, required) — **device id only** (24-char hex from get_inventory `devices[].id`). Never pass MAC (e.g. C6:66:EE:4E:E8:72) or serial_number. Example: `{ "device_ids": ["6108fe9382bcdd7d877ad896", "6108fe9382bcdd7d877ad897"] }`.

### associated_licenses
- method: POST
- path: /orgs/{orgId}/licenses/association
- auth: x-auth-token header
- description: **Bind existing license(s) to device(s).** Request body must be **ids only**: `license_ids` = from **license_candidates** (populated by get_licenses) — match user's license key to **license_key**, use **license_id** (24-char hex); **NEVER use `license_key`** in license_ids or you get 400 Invalid ObjectID. `device_ids` = from **device_candidates** (get_inventory) — use **device_id**, never MAC or serial. Call get_licenses → get_inventory → associated_licenses; resolve ids from license_candidates and device_candidates from the latest API responses. Do not call add_license_key or auto_associated_license_key for this flow.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier (24-char hex). |

#### Query Parameters

(EMPTY)

#### Request Body

Required. JSON object: `license_ids` (array of strings — from **license_candidates**: match user's key to **license_key**, use **license_id**; never put license_key string in license_ids), `device_ids` (array of strings — from **device_candidates** **device_id**; never MAC or serial_number). Example: `{ "license_ids": ["<license_id from license_candidates>"], "device_ids": ["<device_id from device_candidates>"] }`.

### move_licenses_between_orgs
- method: POST
- path: /orgs/{orgId}/licenses/move
- auth: x-auth-token header
- description: Move license(s) from the current org (path orgId) to a target org (body org_id). Use when the user wants to **move license(s) to another organization** (Change Organization; **License** tab → move license to other org). **Only licenses with no device association** (device_id empty in get_licenses response) and **status inactive** can be moved. User must have Org Admin of **both** source and target org. If the user wants to move a license that is already associated with a device, direct them to **move_devices_between_orgs** instead.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | **Source** organization identifier (current org of the licenses). |

#### Query Parameters

(EMPTY)

#### Request Body

Body is a JSON object. Required: `org_id` (string) — **target** organization identifier (24-char hex). Required: `license_ids` (array of strings) — **must be the exact `licenses[].id`** from the **get_licenses** response (same run). When the user specifies a license by key (e.g. 69B8A4-9E6CB3-09DB61-ACA32D), find that license in the get_licenses response and use **that object's `id`** (e.g. 69b8a4b47621a6c1995f9fd5). **Never** put license_key in license_ids. **Never** derive an id from the key (e.g. removing dashes from the key gives a wrong value and causes 406). Only include licenses where status is inactive and device_id is empty. Example: `{ "org_id": "5d3a70dfae4a1400010a36d7", "license_ids": ["<licenses[].id from get_licenses>"] }`.

## Flow Modules (Execution Order)

### F0. Prerequisite Gate (Identifier Resolution)

1. If **`orgId`** is missing or not trusted in context: load skill **`orgs`**, call **`get_user_orgs`**, resolve canonical **`orgId`**. Never pass org **names** as ids.
2. If the task needs **`hvId`** / **`networkId`** / **`hierarchy_view_id`** (assign device, move between networks, create backup, apply template `network_ids`, etc.): load **`hvs`**, call **`get_hierarchy_views`** with resolved **`orgId`**.
3. Multi-org: if **`get_user_orgs`** returns multiple orgs and the user did not specify target org, stop and ask which org.


### F1. List licenses

**`get_licenses`** with **`orgId`**. Filter **`license_type=pro_license`** for Per-Device PRO; **`order`** must be **`+`** or **`-`** only.

### F2. Add key / assign / auto-associate / associated / move licenses

**`add_license_key`**: path **`orgId`** + **`licenseKey`**.

**`assign_license`**: **`get_inventory`** (skill **devices**) for **`deviceId`** — then **`assign_license`**.

**`auto_associated_license_key`**: device **`device_ids`** only from **`get_inventory`** (`devices` skill).

**`associated_licenses`**: Run **`get_licenses`** then **`get_inventory`** so **`license_candidates`** / **`device_candidates`** exist; **`license_ids`** = **`license_id`** only; **`device_ids`** = device id hex only.

**`move_licenses_between_orgs`**: inactive + empty **`device_id`** only; **`license_ids`** from **`get_licenses`** **`licenses[].id`**.

### F4. API Naming and Reference Rule

1. Plain `operation_id`: `get_licenses`, `add_license_key`, `assign_license`, `auto_associated_license_key`, `associated_licenses`, `move_licenses_between_orgs`.

2. If response schema detail is unclear, load `references/<operation_id>.md`.



## Constraints (Hard Rules)

- C1 Canonical **`orgId`** via **`orgs`** **`get_user_orgs`**.
- C3 Operation naming: `get_licenses`, `add_license_key`, `assign_license`, `auto_associated_license_key`, `associated_licenses`, `move_licenses_between_orgs`.
- C5 subset: **`orgId`** hex; **`associated_licenses`** ids from latest **`get_licenses`**/**`get_inventory`**.
- C5b/C5c/C5d: **`associated_licenses`** / **`auto_associated_license_key`** — **`device_ids`** never MAC/serial; **`license_ids`** never license key strings.
- C15 Time display: org timezone from **`get_user_orgs`** when showing license dates.
- C16b **`move_licenses_between_orgs`**: path source org, body target **`org_id`**; **`license_ids`** verbatim from **`get_licenses`**.
- C26 **`order`** on list APIs: exactly **`+`** or **`-`**.
