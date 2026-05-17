---
name: team-members
description: >
  Manage organization and network memberships, including org invite, network role
  updates, membership deletion, and membership overview query.
---

## Persona & Output Rules — MANDATORY

⚠️ **Before responding to any user query that triggers this skill**, ensure `../../references/network-admin-persona.md` is loaded into your context:

- **If this is the first persona-aware skill called in this session**: use the **Read tool** to load it now, before any other action.
- **If you've already read persona.md earlier in this session**: you may rely on context (no need to re-read), but you MUST explicitly confirm to yourself which voice principles and escalation rules from persona.md apply to this query before responding.

The file defines voice principles, vocabulary translation (jargon → SMB-friendly), and the escalation matrix (when to reply with text vs dashboard vs action). Without applying it, the response won't match EnGenius brand voice for SMB customers — a product defect.

**Transparency rule**: if the user asks whether you read persona.md, answer honestly (e.g., "loaded earlier in this session, applied from context" vs "just loaded via Read tool").

# Organization and Network Membership Management

## Quick Reference

| Task                                                         | How                                                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Call any API operation                                       | `python scripts/call_api.py --operation-id OPERATION_ID [--path-params 'JSON'] [--query-params 'JSON'] [--body 'JSON']` |
| Read API schema details                                     | Read `references/<operation_id>.md` (example: [references/get_org_memberships_overall.md](references/get_org_memberships_overall.md)) |
| Validate Email Format                                        | `python ../_shared/scripts/validate_email.py '<email>'`                                     |

### Example

```bash
# Validate email format
python ../_shared/scripts/validate_email.py 'user.com'

# GET — list orgs memberships overall
python scripts/call_api.py --operation-id get_org_memberships_overall --path-params '{"orgId":"<orgId>"}'
```


## API Operations

### create_org_memberships

- method: POST
- path: /orgs/{orgId}/memberships
- auth: x-auth-token header
- description: Invite users to an org membership list.

#### Path Parameters

| name  | type   | required | description                     |
| ----- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body

> Full request body schema and example: see API schema `references/create_org_memberships.md`.

### patch_networks_memberships

- method: PATCH
- path: /orgs/{orgId}/networks/memberships
- auth: x-auth-token header
- description: Invite users to networks, modify network roles, or remove users from networks.

#### Path Parameters

| name  | type   | required | description                     |
| ----- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body

> Full request body schema and example: see API schema `references/patch_networks_memberships.md`.

### delete_org_user_membership

- method: DELETE
- path: /orgs/{orgId}/memberships/{userId}
- auth: x-auth-token header
- description: Remove a specific org user's membership.

#### Path Parameters

| name   | type   | required | description                          |
| ------ | ------ | -------- | ------------------------------------ |
| orgId  | string | true     | Target organization identifier.      |
| userId | string | true     | User identifier in the organization. |

#### Query Parameters

(EMPTY)

#### Request Body

(EMPTY)

### get_org_memberships_overall

- method: GET
- path: /orgs/{orgId}/memberships/overall
- auth: x-auth-token header
- description: Return a list of members from an org and networks.

#### Path Parameters

| name  | type   | required | description                     |
| ----- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier. |

#### Query Parameters

(EMPTY)

#### Request Body

(EMPTY)

#### Response Body

> Full response body schema and example: see API schema `references/get_org_memberships_overall.md`.

### create_org_member_user_invitation

- method: POST
- path: /orgs/{orgId}/memberships/{userId}/invitations
- auth: x-auth-token header
- description: Send the org invitation email to a specific user.

#### Path Parameters

| name   | type   | required | description                     |
| ------ | ------ | -------- | ------------------------------- |
| orgId  | string | true     | Target organization identifier. |
| userId | string | true     | Target user identifier.         |

#### Query Parameters

(EMPTY)

#### Request Body

(EMPTY)

## Flow Modules (Execution Order)

Use the following flow modules in order. Keep each module independent, so adding a new module does not change existing module behavior unless explicitly stated.

### F0. Prerequisite Gate (Identifier Resolution)

1. If required ids are missing, resolve in this order:
   - Load skill `orgs`, then call `get_user_orgs` to resolve canonical `orgId`.
   - If task is network-related and `network_id`/`hierarchy_view_id` is missing, load skill `hvs` and call `get_hierarchy_views` with resolved `orgId`.
   - Use user-provided names only as lookup hints; never pass names/aliases directly as path ids.

### F1. State Discovery

1. After `F0` passes, call `get_org_memberships_overall` to understand current org/network memberships.

### F2. Preflight Validation

Requires F1 to have completed first; current membership state must be known before running any check below.

Before invoking a membership-changing API, MUST run the applicable pre-checks from current state:

1. With org membership create (F3 path — new invite only), MUST run:
   - Email format validity check.
   - Idempotency check: if current role already equals target role, stop early and report no change needed (no API call).
   - Missing context check: if current role state is unknown, resolve first; do not issue blind update calls.
2. With network membership update, MUST run:
   - Legality check: verify requested target roles are allowed by all constraints in `C*` section.
   - Idempotency check: if current role already equals target role, stop early and report no change needed (no API call).
   - Missing context check: if current role state is unknown, resolve first; do not issue blind update calls.

### F3. Create New Membership Path

If email does not exist:

1. Call `create_org_memberships`.
2. Then call `patch_networks_memberships` if network role is requested.

### F4. Org Role Replacement Path (Existing Membership)

If org membership exists and org role must change (for example `admin -> viewer` or `viewer -> admin`):

Note: Email format validation (F2.1) is NOT required — the email is sourced from existing membership state and is already confirmed valid.

1. Ask the user for explicit confirmation before delete.
2. Call `delete_org_user_membership`.
3. Call `create_org_memberships` with the new org role.
4. If delete and following create both succeed, treat task as completed. Do NOT repeat identical delete/create pair.

### F5. Network-Only Role Update Path

If the request is only to add/update a network role:

1. If the target email does NOT exist in current org membership state, stop early. Explain that network-only role update requires an existing org membership first. Do NOT call `patch_networks_memberships`.
2. If org membership already exists AND org role does NOT need to change, do NOT call `delete_org_user_membership` or `create_org_memberships` (org membership is unchanged).
3. Call `patch_networks_memberships` with the target network role only after step 2 is satisfied.
4. Do NOT enter F4; F4 only applies when org role replacement is explicitly required.

### F6. Membership Deletion Path (Pure Deletion)

If the user explicitly requests to remove or delete a user from an org:

1. Do NOT proceed with deletion unless the user has explicitly confirmed with "Yes" in the immediately preceding turn.
2. If confirmation is missing, stop and ask: "Are you sure you want to remove [email] from [org]?" Do not call any API.
3. Only after the user confirms, call `delete_org_user_membership`.

### F7. Completion Convergence

For mutation operations:

- If latest successful mutation is `create_org_memberships` or `patch_networks_memberships`, next step MUST be:
  - call exactly one `get_org_memberships_overall` for verification, then
  - respond to the user with the result.
- For other successful mutations, next step must be either:
  - respond to the user directly, or
  - at most one read verification (`get_org_memberships_overall`) then respond to the user with the result.
- Never repeat the same mutation call with identical payload/path params after success.

### F8. Final Response Accuracy

- Final user-facing role/result must match latest successful target role in request payload.
- Do not reuse stale role wording from older session history.

### F9. Operation Naming Rule

- When invoking an API operation, use only the plain `operation_id` (e.g. `create_org_memberships`).
- Do NOT prefix with skill name (e.g. do NOT use `team-members.create_org_memberships`).
- If request/response schema detail is unclear in any flow, load the reference schema from `references/<single-api-schema>.md`.

## Constraints (Hard Rules)

These constraints are independent from flow modules. New constraints should be appended as new `C*` items without rewriting existing ones.

- C1 Role domain:
  - Organization roles: `admin`, `viewer`.
  - Network roles: `admin`, `viewer`, `frontdesk`.
- C2 Role legality matrix:
  - Org `admin` cannot be assigned network `viewer` or `frontdesk`.
  - If target network role is `frontdesk` or `viewer`, org permission should be `viewer` or `none`.
  - If org permission is `viewer`, network permission can be `admin` or `viewer`.
  - If org permission is `none`, network permission can include `frontdesk`.
