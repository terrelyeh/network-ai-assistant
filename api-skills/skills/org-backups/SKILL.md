---
name: org-backups
description: >
  Network backups: create, list, restore, patch (protect/re-backup/rename),
  delete.
---

## Persona & Output Rules — MANDATORY

⚠️ **Before responding to any user query that triggers this skill**, ensure `../../references/network-admin-persona.md` is loaded into your context:

- **If this is the first persona-aware skill called in this session**: use the **Read tool** to load it now, before any other action.
- **If you've already read persona.md earlier in this session**: you may rely on context (no need to re-read), but you MUST explicitly confirm to yourself which voice principles and escalation rules from persona.md apply to this query before responding.

The file defines voice principles, vocabulary translation (jargon → SMB-friendly), and the escalation matrix (when to reply with text vs dashboard vs action). Without applying it, the response won't match EnGenius brand voice for SMB customers — a product defect.

**Transparency rule**: if the user asks whether you read persona.md, answer honestly (e.g., "loaded earlier in this session, applied from context" vs "just loaded via Read tool").

# Organization Network Backups

## Quick Reference

| Task | How |
|------|-----|
| Call any API operation | `python scripts/call_api.py --operation-id OPERATION_ID [--path-params 'JSON'] [--query-params 'JSON'] [--body 'JSON']` |
| Read API schema details | Read `references/<operation_id>.md` |

### Example

```bash
python scripts/call_api.py --operation-id get_org_backups --path-params '{"orgId":"<orgId>"}'
```

## API Operations

For each operation below, full request/response schema details are in `references/<operation_id>.md`.

### create_org_backup
- method: POST
- path: /orgs/{orgId}/backups
- auth: x-auth-token header
- description: Create a new network-wide setting and device backup in the org. Use when the user wants to create a network backup. Request body is required: name, hierarchy_view_id, network_id; optional description, is_protected (boolean).

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body

Required. JSON object: `name` (string), `hierarchy_view_id` (string, from get_hierarchy_views), `network_id` (string, from hierarchy view networks), optional `description` (string), optional `is_protected` (boolean). Example: `{ "name": "Backup", "hierarchy_view_id": "59d72645g799c000126e38e", "network_id": "59d72645g799c000126e388", "is_protected": true, "description": "" }`.

### get_org_backups
- method: GET
- path: /orgs/{orgId}/backups
- auth: x-auth-token header
- description: Return a list of backups under the org. Use when the user asks for backup list or when you need to resolve backupId by backup name for restore_network_backup or patch_org_backup. **Candidate mapping:** successful response is normalized into **org_backup_candidates** (backup_id, name, network_name) for later backupId resolution.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

| name | type   | required | default | description |
| ---- | ------ | -------- | ------- | ----------- |
| from | integer | false | 0 | Pagination start index. |
| count | integer | false | 10 | Number of items to return. |
| order | string | false | + | Sort order: `+` (asc) or `-` (desc). Pass `+` or `-` only. |
| sort | string | false | name | Sort field: name, network_name, creator, created_time, snapshot_time. |
| search | string | false | none | Search in name, network_name, creator. |

#### Request Body

(EMPTY)

### delete_org_backups
- method: DELETE
- path: /orgs/{orgId}/backups
- auth: x-auth-token header
- description: Delete backups under the org. Use when the user wants to delete one or more network backups. Resolve orgId from get_user_orgs; resolve backup IDs **only** from **get_org_backups** response (backups[].id) or **org_backup_candidates** (match backup **name** to user request, use that entry's **backup_id**). Request body is required: JSON array of backup id strings. Protected backups may be restricted from deletion.

**Pure deletion:** Do **not** call this API unless the user has explicitly confirmed (e.g. "Yes") in the **immediately preceding** turn for deleting the named backup(s). If confirmation is missing, stop and ask: "Are you sure you want to delete the selected backup(s)?" (use backup name(s) when known). Do not call any API until confirmed. Only after confirmation, call `delete_org_backups`.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body (OpenAPI: `Array[string]`)

**Request body must be the array itself** — same rule as **delete_network_templates**. ✗ `{"backupIds":["..."]}` ✓ `["..."]`. Example: `["59d72645g799c000126e388"]`. Ids from get_org_backups **backups[].id** or **org_backup_candidates** **backup_id**.

### restore_network_backup
- method: POST
- path: /orgs/{orgId}/backups/{backupId}/restoration
- auth: x-auth-token header
- description: Restore the network from a backup. Restores all settings (Network-wide settings and Device settings) to the corresponding network. Use when the user wants to restore a network from an existing backup. Resolve orgId from get_user_orgs; resolve backupId **only** from the **get_org_backups response** of the previous step (see path param below).

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |
| backupId | string | true     | From **org_backup_candidates** (built from get_org_backups): match backup **name** to user request, use that entry's **backup_id**. Do NOT use network_id or other lists — wrong id → 404. |

#### Query Parameters

(EMPTY)

#### Request Body

(EMPTY)

### patch_org_backup
- method: PATCH
- path: /orgs/{orgId}/backups/{backupId}
- auth: x-auth-token header
- description: Update a backup under the org. **Three cases (same path):** **(1) Protect** — body `{ "is_protected": true }` or `false` so the backup is not rotated when exceeding 2 backups of the network; **(2) Re-Backup** — body `{ "is_updated": true }` to refresh the backup with current network/device settings; **(3) Modify name/description** — body `{ "name": "<string>", "description": "<string>" }`; send only the field(s) to change. Resolve orgId from get_user_orgs; resolve backupId **only** from **get_org_backups** response (backups[].id).

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |
| backupId | string | true     | From **org_backup_candidates** (filled by get_org_backups): match backup **name** to user request, use that entry's **backup_id**. Do NOT use network_id — wrong id → 404. |

#### Query Parameters

(EMPTY)

#### Request Body

JSON object with **only** the fields for the intended case: `is_protected` (boolean) for Protect; `is_updated: true` for Re-Backup; `name` and/or `description` (string) for Modify. Example: `{ "is_protected": true }`; `{ "is_updated": true }`; `{ "name": "New name", "description": "" }`.

## Flow Modules (Execution Order)

### F0. Prerequisite Gate (Identifier Resolution)

1. If **`orgId`** is missing or not trusted in context: load skill **`orgs`**, call **`get_user_orgs`**, resolve canonical **`orgId`**. Never pass org **names** as ids.
2. If the task needs **`hvId`** / **`networkId`** / **`hierarchy_view_id`** (assign device, move between networks, create backup, apply template `network_ids`, etc.): load **`hvs`**, call **`get_hierarchy_views`** with resolved **`orgId`**.
3. Multi-org: if **`get_user_orgs`** returns multiple orgs and the user did not specify target org, stop and ask which org.


### F1. Create backup

1. **`get_hierarchy_views`** → **`create_org_backup`** with **`name`**, **`hierarchy_view_id`**, **`network_id`** from HV response.

### F2. List / restore / patch / delete

1. **`get_org_backups`** for list and **`backupId`** resolution (**`org_backup_candidates`**).
2. Restore: **`restore_network_backup`**. Patch: **`patch_org_backup`**. Delete: **`delete_org_backups`** — body is **JSON array root** of ids — not wrapped object.

### F3. API Naming

Plain ids: `create_org_backup`, `get_org_backups`, `delete_org_backups`, `restore_network_backup`, `patch_org_backup`.

1. If response schema detail is unclear, load `references/<operation_id>.md`.

### F4. Pure Deletion Paths (Destructive DELETE APIs)

1. **Applies to:** **`delete_org_backups`** — user confirmation per **Pure deletion** in API Operations.
2. When the user explicitly asks to delete backups: do not call **`delete_org_backups`** until they have clearly confirmed (preferably "Yes" in the immediately preceding turn). If confirmation is missing, stop and ask using the wording in **Pure deletion**.
3. **Multi-turn:** Do not summarize success as done while only asking confirmation.

## Constraints (Hard Rules)

- C1 **`orgId`** from **`orgs`**.
- C3 **`operation_id`** plain: `create_org_backup`, `get_org_backups`, `delete_org_backups`, `restore_network_backup`, `patch_org_backup`.
- C19 **`backupId`** from **`get_org_backups`** / **`org_backup_candidates`** — never **`network_id`**.
- C24b **`delete_org_backups`** body = root JSON array of backup id strings.
- C26 **`order`** on **`get_org_backups`**: **`+`** or **`-`** only.
