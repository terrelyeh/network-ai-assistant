---
name: hvs
description: >
  Resolve hierarchy views and networks under an org. Use this skill to discover
  hierarchy_view_id and network_id from org structure .
---

## Persona & Output Rules — MANDATORY

⚠️ **Before responding to any user query that triggers this skill**, ensure `../../references/network-admin-persona.md` is loaded into your context:

- **If this is the first persona-aware skill called in this session**: use the **Read tool** to load it now, before any other action.
- **If you've already read persona.md earlier in this session**: you may rely on context (no need to re-read), but you MUST explicitly confirm to yourself which voice principles and escalation rules from persona.md apply to this query before responding.

The file defines voice principles, vocabulary translation (jargon → SMB-friendly), and the escalation matrix (when to reply with text vs dashboard vs action). Without applying it, the response won't match EnGenius brand voice for SMB customers — a product defect.

**Transparency rule**: if the user asks whether you read persona.md, answer honestly (e.g., "loaded earlier in this session, applied from context" vs "just loaded via Read tool").

# Hierarchy View and Network Discovery

## Quick Reference

| Task | How |
|------|-----|
| Call any API operation | `python scripts/call_api.py --operation-id OPERATION_ID [--path-params 'JSON'] [--query-params 'JSON'] [--body 'JSON']` |
| Read API schema details | Read `references/<operation_id>.md` (example: [references/get_hierarchy_views.md](references/get_hierarchy_views.md)) |

### Example

```bash
# GET — list hierarchy views and networks under an org
python scripts/call_api.py --operation-id get_hierarchy_views --path-params '{"orgId":"<orgId>"}'
```


## API Operations

### get_hierarchy_views
- method: GET
- path: /orgs/{orgId}/hvs
- auth: x-auth-token header
- description: Return hierarchy views and networks of the org.

#### Path Parameters
| name | type | required | description |
|---|---|---|---|
| orgId | string | true | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body

(EMPTY)

## Flow Modules (Execution Order)

Use the following flow modules in order. Keep each module independent, so adding a new module does not change existing module behavior unless explicitly stated.

### F0. Prerequisite Gate

1. `orgId` is required before calling `get_hierarchy_views`.
2. If `orgId` is missing, resolve it first via the `orgs` skill (`get_user_orgs`).

### F1. Fetch Hierarchy and Network Context

1. If target `orgId` is known/specified, call `get_hierarchy_views` with that canonical `orgId`.
2. If user asks about a network name but org is not specified and multiple orgs are available, call `get_hierarchy_views` for each candidate org and aggregate results.
3. Treat returned hierarchy/network list as source of truth.
4. Do not early-stop because call count is high; repeated `get_hierarchy_views` calls across many orgs are expected. Continue until full candidate-org scan is complete or iteration limit is reached.

### F2. Identifier Extraction

1. Extract and keep `hierarchy_view_id` and network `id` for downstream membership patch actions.
2. If user specifies network name, match from returned `networks` list before selecting ids.

### F3. Ambiguity Handling

1. For "which org contains network <name>" queries:
   - If multiple orgs have the same network name, list every matched org in the response.
   - Do NOT collapse multiple matches into a single org.
2. For mutation/downstream action queries:
   - If network name lookup has multiple matches or no reliable match, stop and ask user to clarify target org/network before proceeding.
3. Do not issue blind downstream mutations with uncertain network mapping.

### F4. API Naming and Reference Rule

1. When invoking an API operation, use only the plain `operation_id` as defined in the `## API Operations` section above.
2. If response schema detail is unclear, load the operation-specific reference schema from `references/<operation_id>.md`.

### F5. Handoff

1. Pass selected canonical `hv_id` and `network_id` to downstream skills (`hvs`, `org-network-groups`, `org-network-templates`, `org-devices` or `team-members`).
2. Do not continue with org-dependent operations until `org_id` is resolved.

## Constraints (Hard Rules)

These constraints are independent from flow modules. New constraints should be appended as new `C*` items without rewriting existing ones.

- C1 Canonical identifier guard:
  - Do not fabricate hierarchy/network identifiers.
  - Use only ids resolved from `get_hierarchy_views` response.
- C2 orgId prerequisite guard:
  - Do NOT call `get_hierarchy_views` without canonical `orgId`.
- C3 Ambiguity guard:
  - For location queries ("which org has network X"), if multiple orgs match, return all matched orgs.
  - For mutation/downstream actions, if network selection is ambiguous, do NOT auto-pick; ask the user to clarify.
- C4 Operation naming guard:
  - Use the operation `get_hierarchy_views` as defined in the API Operations section.
- C5 Output scope:
  - Keep response focused on ids/names required by next actions.
- C6 Cross-org search guard:
  - If org is unspecified and multiple orgs exist, network-name lookup must evaluate each org by calling `get_hierarchy_views` per org.
- C7 High-volume scan guard:
  - A large number of orgs is normal; many repeated `get_hierarchy_views` calls are allowed.
  - Do NOT treat high call count alone as an error or stop condition.
