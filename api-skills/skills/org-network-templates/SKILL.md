---
name: org-network-templates
description: >
  Network templates (clone from eligible network, list/patch/delete/apply).
---

## Persona & Output Rules — MANDATORY

⚠️ **Before responding to any user query that triggers this skill**, ensure `../../references/network-admin-persona.md` is loaded into your context:

- **If this is the first persona-aware skill called in this session**: use the **Read tool** to load it now, before any other action.
- **If you've already read persona.md earlier in this session**: you may rely on context (no need to re-read), but you MUST explicitly confirm to yourself which voice principles and escalation rules from persona.md apply to this query before responding.

The file defines voice principles, vocabulary translation (jargon → SMB-friendly), and the escalation matrix (when to reply with text vs dashboard vs action). Without applying it, the response won't match EnGenius brand voice for SMB customers — a product defect.

**Transparency rule**: if the user asks whether you read persona.md, answer honestly (e.g., "loaded earlier in this session, applied from context" vs "just loaded via Read tool").

# Organization Network Configuration Templates

## Quick Reference

| Task | How |
|------|-----|
| Call any API operation | `python scripts/call_api.py --operation-id OPERATION_ID [--path-params 'JSON'] [--query-params 'JSON'] [--body 'JSON']` |
| Read API schema details | Read `references/<operation_id>.md` |

### Example

```bash
python scripts/call_api.py --operation-id get_network_templates --path-params '{"orgId":"<orgId>"}'
```

## API Operations

For each operation below, full request/response schema details are in `references/<operation_id>.md`.

### get_network_template_candidates
- method: GET
- path: /orgs/{orgId}/network-templates/candidates
- auth: x-auth-token header
- description: Return networks that can be used as the source when creating a network template (Add Network template — select network to copy from). **Call this before create_network_template** so the chosen network is confirmed eligible. **Candidate mapping:** successful response is extracted into **org_network_template_candidates** (network_id, name) for later network_id resolution in create_network_template. **Must know:** Only networks that satisfy template constraints (no multiple gateways/switches/cameras/PDUs; no AP overriding network-wide settings) appear here.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body

(EMPTY)

### create_network_template
- method: POST
- path: /orgs/{orgId}/network-templates
- auth: x-auth-token header
- description: Create a Configuration Template by cloning from an existing network. Use **only after** **get_network_template_candidates** in the same flow. Resolve orgId from get_user_orgs; resolve body **network_id** from **org_network_template_candidates** (built from get_network_template_candidates): match the user's source network **name** to the entry's **name**, use that entry's **network_id**. **Do NOT** use network_id from get_hierarchy_views or network_candidates — if the network is not in org_network_template_candidates, it is not eligible; inform the user of template constraints.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body

Required. JSON object: `name` (string), `network_id` (string — **from org_network_template_candidates** only: match user’s source network name to **name**, use **network_id**), optional `description` (string). Example: `{ "name": "Template 1", "network_id": "<from org_network_template_candidates>", "description": "Template 1 Description" }`.

### get_network_templates
- method: GET
- path: /orgs/{orgId}/network-templates
- auth: x-auth-token header
- description: Return a list of network templates under the org. Use when the user asks for Configuration Template list (Organization > Backup & Restore > Configuration Template). Response includes name, template summary (config_summary), last modify time, modify by, note (description), applied_network_ids. **Candidate mapping:** successful response → **org_configuration_template_candidates** (template_id, name) for resolving **templateId** on patch / apply / delete-by-name flows.

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
| sort | string | false | name | Sort field: name, modified_time, modified_by. |

#### Request Body

(EMPTY)

### patch_network_template
- method: PATCH
- path: /orgs/{orgId}/network-templates/{templateId}
- auth: x-auth-token header
- description: Update a configuration template’s name and/or description. Resolve **templateId** from **get_network_templates** `templates[].id` or **org_configuration_template_candidates** (match user’s template name to **name**, use **template_id**).

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |
| templateId | string | true     | From get_network_templates **templates[].id** or org_configuration_template_candidates **template_id**. |

#### Query Parameters

(EMPTY)

#### Request Body

JSON object; include at least one field. **OpenAPI marks requestBody required** — send only fields to change.

| name | type | required | description |
| ---- | ---- | -------- | ----------- |
| name | string | false | New template display name. |
| description | string | false | Note / description (max 255). |

### delete_network_templates
- method: DELETE
- path: /orgs/{orgId}/network-templates
- auth: x-auth-token header
- description: Delete one or more configuration templates under the org. Resolve template ids **only** from **get_network_templates** `templates[].id` or **org_configuration_template_candidates** (**template_id**). **Request body must be the id array at root** (see Request Body below — not an object). Destructive — confirm with user first.

**Pure deletion:** Do **not** call this API unless the user has explicitly confirmed (e.g. "Yes") in the **immediately preceding** turn for deleting the named template(s). If confirmation is missing, stop and ask: "Are you sure you want to delete the selected configuration template(s)?" Do not call any API until confirmed. Only after confirmation, call `delete_network_templates`.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body (OpenAPI: `Array[string]` — no object wrapper)

**Request body must be the array itself**, not a JSON object. The HTTP body is exactly `["id1","id2"]` (Content-Type application/json).

| ✗ WRONG (object — validator strips keys → empty body → backend `$in needs an array` / 500) | ✓ CORRECT |
| --- | --- |
| `{"templateIds": ["69ba42d36c0f3d954e4e925b"]}` | `["69ba42d36c0f3d954e4e925b"]` |
| `{"ids": ["..."]}` | `["..."]` |

Resolve each string from **get_network_templates** `templates[].id` or **org_configuration_template_candidates** **template_id** (match template name → **template_id**).

### apply_network_template
- method: POST
- path: /orgs/{orgId}/network-templates/{templateId}/apply
- auth: x-auth-token header
- description: Apply a template’s stored configuration to target networks (Organization > Configuration Template > Apply). First-time apply in UI: user may name a network group or pick networks — API accepts **network_ids** only. Resolve **network_ids** from **get_hierarchy_views** (`networks[].id`) when the user names specific networks, or from **get_network_groups** `groups[].network_ids` when applying to all networks in a group. Resolve **templateId** from **get_network_templates** or **org_configuration_template_candidates**.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |
| templateId | string | true     | Template to apply; from get_network_templates **templates[].id** or org_configuration_template_candidates **template_id**. |

#### Query Parameters

(EMPTY)

#### Request Body

| name | type | required | description |
| ---- | ---- | -------- | ----------- |
| network_ids | array | true | Network id strings: from **get_hierarchy_views** `networks[].id` and/or **get_network_groups** `groups[].network_ids`. |

## Flow Modules (Execution Order)

### F1. Prerequisite Gate (Identifier Resolution)

Resolve **`orgId`** from **`get_user_orgs`** (24-char hex). Resolve **`hvId`** and **`networkId`** from **`get_hierarchy_views`** when needed.

1. If **`orgId`** is missing or not trusted in context: load skill **`orgs`**, call **`get_user_orgs`**, resolve canonical **`orgId`**. Never pass org **names** as ids.
2. If the task needs **`hvId`** / **`networkId`** / **`hierarchy_view_id`** (assign device, move between networks, create backup, apply template `network_ids`, etc.): load **`hvs`**, call **`get_hierarchy_views`** with resolved **`orgId`**.
3. Multi-org: if **`get_user_orgs`** returns multiple orgs and the user did not specify target org, stop and ask which org.


### F2. Create template

Create network template by cloning from eligible network. Resolve **`network_id`** from **`org_network_template_candidates`** obtained via **`get_network_template_candidates`**.

1. **`get_network_template_candidates`** → pick **`network_id`** only from **`org_network_template_candidates`** → **`create_network_template`**.

### F3. List / rename / delete / apply templates

Get **`templateId`** from **`get_network_templates`** response. Apply template to networks by resolving **`network_ids`** from **`get_hierarchy_views`** and/or **`get_network_groups`**.

1. **`get_network_templates`** fills **`org_configuration_template_candidates`**.

2. Apply: **`get_network_templates`** for **`templateId`** — build **`network_ids`** from **`get_hierarchy_views`** and/or **`get_network_groups`** (skill **network_groups**).

### F4. API Naming and Reference Rule

Reference guide for API operation naming and schema details.

1. Use plain `operation_id`: `get_network_template_candidates`, `create_network_template`, `get_network_templates`, `patch_network_template`, `delete_network_templates`, `apply_network_template`.

2. If response schema detail is unclear, load `references/<operation_id>.md`.


### F5. Pure Deletion Paths (Destructive DELETE APIs)

Confirmation protocol for destructive operations. Require explicit user confirmation before calling `delete_network_templates`. Body must be root JSON array of template ids.

1. **Applies to:** **`delete_network_templates`** — confirm first; body is root JSON array of template ids.

2. When the user explicitly asks to delete templates: do not call **`delete_network_templates`** until they have clearly confirmed. If confirmation is missing, stop and ask per **Pure deletion**.

3. **Multi-turn:** Do not summarize success as done while only asking confirmation.




## Constraints (Hard Rules)

- C1 **`create_network_template`**: **`network_id`** only from **`org_network_template_candidates`**.
- C2 **`templateId`** from **`get_network_templates`** / **`org_configuration_template_candidates`**.
- C3 **`delete_network_templates`**: root JSON array body.
- C4 **`apply_network_template`**: **`network_ids`** only from HV / network groups.
- C5 **`order`** on **`get_network_templates`**: **`+`**/**`-`** only.
