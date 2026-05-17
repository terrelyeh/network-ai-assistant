---
name: org-network-groups
description: >
  Network groups (bundle of networks): list, create, patch membership,
  delete.
---

## Persona & Output Rules — MANDATORY

⚠️ **Before responding to any user query that triggers this skill**, ensure `../../references/network-admin-persona.md` is loaded into your context:

- **If this is the first persona-aware skill called in this session**: use the **Read tool** to load it now, before any other action.
- **If you've already read persona.md earlier in this session**: you may rely on context (no need to re-read), but you MUST explicitly confirm to yourself which voice principles and escalation rules from persona.md apply to this query before responding.

The file defines voice principles, vocabulary translation (jargon → SMB-friendly), and the escalation matrix (when to reply with text vs dashboard vs action). Without applying it, the response won't match EnGenius brand voice for SMB customers — a product defect.

**Transparency rule**: if the user asks whether you read persona.md, answer honestly (e.g., "loaded earlier in this session, applied from context" vs "just loaded via Read tool").

# Organization Network Groups

## Quick Reference

| Task | How |
|------|-----|
| Call any API operation | `python scripts/call_api.py --operation-id OPERATION_ID [--path-params 'JSON'] [--query-params 'JSON'] [--body 'JSON']` |
| Read API schema details | Read `references/<operation_id>.md` |

### Example

```bash
python scripts/call_api.py --operation-id get_network_groups --path-params '{"orgId":"<orgId>"}'
```

## API Operations

For each operation below, full request/response schema details are in `references/<operation_id>.md`.

### get_network_groups
- method: GET
- path: /orgs/{orgId}/network-groups
- auth: x-auth-token header
- description: Return all network groups under the org. Response **groups**: each has **id**, **name**, **network_ids**. **Candidate mapping:** successful response → **org_network_group_candidates** (group_id, name) for resolving **groupId** when user refers to a group by name (patch/delete).

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body

(EMPTY)

### create_network_group
- method: POST
- path: /orgs/{orgId}/network-groups
- auth: x-auth-token header
- description: Create a network group under the org (bundle of networks). Resolve **network_ids** from hvs **get_hierarchy_views** (networks under each hierarchy view). Body: **name** (string), **network_ids** (string array). OpenAPI file lists a typo **networks_ids**; use **network_ids** (same as GET response).

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body

Required. JSON object: `name` (string), `network_ids` (array of network id strings from get_hierarchy_views). Example: `{ "name": "Network Group 1", "network_ids": ["<networkId1>", "<networkId2>"] }`.

### patch_network_group
- method: PATCH
- path: /orgs/{orgId}/network-groups/{groupId}
- auth: x-auth-token header
- description: Update a network group. **`network_ids` on PATCH = full member list.** **Pipeline to remove network(s) from a group:** **(1)** **get_network_groups** — use **this GET response** only. **(2)** **get_hierarchy_views** — **`network_id_to_remove`** = `networks[].id` where `networks[].name` matches user’s network to delete. **(3)** In step (1), find target group; copy its full **`network_ids`**. **(4)** **`network_ids_remaining`** = that array with **only** **`network_id_to_remove`** removed (repeat for multiple removals). **(5)** **patch_network_group** (`orgId`, `groupId` = group’s `id`, body `{ "network_ids": network_ids_remaining }`). follow steps (1)–(5) so removing one network does not become an accidental full clear.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |
| groupId | string | true     | Group id from get_network_groups **groups[].id** or org_network_group_candidates **group_id**. |

#### Query Parameters

(EMPTY)

#### Request Body

JSON object. **Remove network from group:** after steps above, `{ "network_ids": [<every id from get_network_groups for that group except network_id_to_remove>] }`.

### delete_network_group
- method: DELETE
- path: /orgs/{orgId}/network-groups/{groupId}
- auth: x-auth-token header
- description: Delete a network group under the org. Resolve **groupId** from **get_network_groups** or **org_network_group_candidates** (match by name).

**Pure deletion:** Do **not** call this API unless the user has explicitly confirmed (e.g. "Yes") in the **immediately preceding** turn for deleting this network group. If confirmation is missing, stop and ask: "Are you sure you want to delete this network group?" (use group name when known). Do not call any API until confirmed. Only after confirmation, call `delete_network_group`.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |
| groupId | string | true     | Group id from get_network_groups **groups[].id** or org_network_group_candidates **group_id**. |

#### Query Parameters

(EMPTY)

#### Request Body

(EMPTY)

## Flow Modules (Execution Order)

### F1. Prerequisite Gate (Identifier Resolution)

Resolve **`orgId`** from **`get_user_orgs`** (24-char hex). Resolve **`hvId`** and **`networkId`** from **`get_hierarchy_views`** when needed.

1. If **`orgId`** is missing or not trusted in context: load skill **`orgs`**, call **`get_user_orgs`**, resolve canonical **`orgId`**. Never pass org **names** as ids.
2. If the task needs **`hvId`** / **`networkId`** / **`hierarchy_view_id`** (assign device, move between networks, create backup, apply template `network_ids`, etc.): load **`hvs`**, call **`get_hierarchy_views`** with resolved **`orgId`**.
3. Multi-org: if **`get_user_orgs`** returns multiple orgs and the user did not specify target org, stop and ask which org.


### F2. List / create / patch / delete groups

Get **`groupId`** from **`get_network_groups`** response (`groups[].id`). Resolve **`networkId`** from **`get_hierarchy_views`** for group operations.

1. Create: **`get_hierarchy_views`** for **`network_ids`** → **`create_network_group`**.

2. Remove network from group: **`get_network_groups`** → **`get_hierarchy_views`** for id to remove → compute full **`network_ids`** minus removed → **`patch_network_group`**.

3. Delete group: **`delete_network_group`** — confirm per **Pure deletion**.

### F3. API Naming and Reference Rule

Reference guide for API operation naming and schema details.

1. Use plain `operation_id`: `get_network_groups`, `create_network_group`, `patch_network_group`, `delete_network_group`.

2. If response schema detail is unclear, load `references/<operation_id>.md`.


### F4. Pure Deletion Paths (Destructive DELETE APIs)

Confirmation protocol for destructive operations. Require explicit user confirmation before calling `delete_network_group`.

1. **Applies to:** **`delete_network_group`**.

2. When the user explicitly asks to delete a group: do not call **`delete_network_group`** until they have clearly confirmed. If confirmation is missing, stop and ask per **Pure deletion**.

3. **Multi-turn:** Do not summarize success as done while only asking confirmation.




## Constraints (Hard Rules)

- C1 **`groupId`** from **`get_network_groups`** / **`org_network_group_candidates`**.
- C2 Remove-member pipeline: **`get_network_groups`** → **`get_hierarchy_views`** → **`patch_network_group`** with full remaining **`network_ids`**.
- C3 **`order`** where applicable: **`+`**/**`-`** only.
