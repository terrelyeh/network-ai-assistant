---
name: init-orgs
description: >
  Resolve organization context (org_id): list organizations for the user, read/update
  org-level settings (feature plan per device type, country, time_zone settings)
  Use this skill to fetch org_id before calling hierarchy-view, org-backups, org-devices, org-licenses,
  org-network-groups, org-network-templates or membership APIs.
---

## Persona & Output Rules — MANDATORY

⚠️ **Before responding to any user query that triggers this skill**, ensure `../../references/network-admin-persona.md` is loaded into your context:

- **If this is the first persona-aware skill called in this session**: use the **Read tool** to load it now, before any other action.
- **If you've already read persona.md earlier in this session**: you may rely on context (no need to re-read), but you MUST explicitly confirm to yourself which voice principles and escalation rules from persona.md apply to this query before responding.

The file defines voice principles, vocabulary translation (jargon → SMB-friendly), and the escalation matrix (when to reply with text vs dashboard vs action). Without applying it, the response won't match EnGenius brand voice for SMB customers — a product defect.

**Transparency rule**: if the user asks whether you read persona.md, answer honestly (e.g., "loaded earlier in this session, applied from context" vs "just loaded via Read tool").

# Organization Context

## Intents

- **List orgs / resolve `orgId`**: **`get_user_orgs`** — each org includes feature plan fields (`ap_license_mode`, …), `country`, **`time_zone`** (IANA). Use **`time_zone`** when presenting dates (see C15).
- **Org-level settings**: **`patch_org`** — feature plan (`*_license_mode` basic/pro) and/or Exposure Analysis (`is_exposure_analysis_enable`).

For device inventory or license-expiry summary (widget), use skill **org-devices**.

For inventory, devices on networks, licenses tab operations, backups, templates, or groups, load the skill listed in the description above — do not assume those APIs live in **`orgs`**.

## Quick Reference

| Task | How |
|------|-----|
| Call any API operation | `python scripts/call_api.py --operation-id OPERATION_ID [--path-params 'JSON'] [--query-params 'JSON'] [--body 'JSON']` |
| Read API schema details | Read `references/<operation_id>.md` |

### Example

```bash
python scripts/call_api.py --operation-id get_user_orgs
```

## API Operations

For each operation below, full request/response schema details are in `references/<operation_id>.md`.

### get_user_orgs
- method: GET
- path: /user/orgs
- auth: x-auth-token header
- description: Returns a list of orgs for the authenticated user. Each org includes **FEATURE PLAN** (license plan per device type): `ap_license_mode`, `switch_license_mode`, `gateway_license_mode`, `pdu_license_mode`, `switch_extender_license_mode`, `camera_license_mode`, `nvs_license_mode` — these correspond to the UI row (e.g. PRO AP, PRO SW, PRO GW, PRO PDU, PRO EXT). Use when the user asks about feature plan, PRO status, or license plan by device type. Each org also has `country` and `time_zone` (IANA); when presenting date/time to the user, use the selected org's `time_zone` (see C15).

#### Path Parameters

(EMPTY)

#### Query Parameters

(EMPTY)

#### Request Body

(EMPTY)

#### Response Body

> Full response body schema and example: see API schema `references/get_user_orgs.md`.

### patch_org
- method: PATCH
- path: /orgs/{orgId}
- auth: x-auth-token header
- description: Update org settings. **Two cases (same path):** **(1) Feature plan per device type** — send one or more of `ap_license_mode`, `switch_license_mode`, `gateway_license_mode`, `pdu_license_mode` (each `basic` or `pro`); **(2) Exposure Analysis** — send `is_exposure_analysis_enable` (boolean) to enable/disable timeline of clients connected to the same AP. Resolve orgId from get_user_orgs.

#### Path Parameters

| name | type   | required | description                     |
| ---- | ------ | -------- | ------------------------------- |
| orgId | string | true     | Target organization identifier (from get_user_orgs). |

#### Query Parameters

(EMPTY)

#### Request Body

- **Feature plan:** JSON object with optional `ap_license_mode`, `switch_license_mode`, `gateway_license_mode`, `pdu_license_mode` (each `basic` or `pro`). Send only the field(s) to change. Example: `{ "ap_license_mode": "pro" }`.
- **Exposure Analysis:** JSON object with `is_exposure_analysis_enable` (boolean). Example: `{ "is_exposure_analysis_enable": true }`.

## Flow Modules (Execution Order)

### F0. Trigger Gate

1. Use this skill when **`orgId`** is required but missing or untrusted.
2. If **`orgId`** is already resolved and trusted, do **not** repeat **`get_user_orgs`** unnecessarily.

### F1. Fetch Organization Context

1. Call **`get_user_orgs`** to retrieve available organizations.
2. Treat returned org list as source of truth for canonical **`org_id`** and **`time_zone`**.

### F2. Selection and Disambiguation

1. If only one org is available, use that **`org_id`**.
2. If multiple orgs exist and the user did not specify target org, stop and ask the user to choose.

### F3. Org-level mutations

1. Pass selected canonical org_id to downstream skills (hvs, org-backups, org-devices, org-licenses, org-network-groups, org-network-templates or team-members).
2. Do not continue with org-dependent operations until org_id is resolved.

### F4. Org-level mutations

1. **Feature plan / Exposure Analysis:** Call **`patch_org`** with **`orgId`** and only the fields to change (see API Operations).

### F5. API Naming and Reference Rule

1. Use plain **`operation_id`**: **`get_user_orgs`**, **`patch_org`**. Do **not** prefix with skill name.
2. If schema detail is unclear, load **`references/<operation_id>.md`**.

## Constraints (Hard Rules)

- C1 Canonical org identifier: Never guess **`org_id`** — resolve only from **`get_user_orgs`** (or downstream structured memory populated from it).
- C2 Disambiguation: Multiple orgs and no explicit target → ask the user; do not auto-pick.
- C3 Operation naming: **`operation_id`** must be exactly **`get_user_orgs`** or **`patch_org`**.
- C4 Output scope: Concise org identifiers/names for downstream steps; omit empty fields.
- C7 Response field semantics: Present fields that match the user question.
- C8 Do not expose internal IDs unless the user asks (still resolve **`orgId`** correctly for API calls).
- C15 Time presentation: When showing dates/times tied to org data, convert using the selected org’s **`time_zone`** from **`get_user_orgs`** for the resolved **`orgId`**.
