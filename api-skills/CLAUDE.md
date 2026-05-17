# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A collection of AI agent skills for the Engenius Cloud management system. Each skill lets an agent interact with the management REST API. The skills are loaded at runtime by an agent harness — `SKILL.md` in each directory is both the documentation and the machine-parseable source of truth for API operations.

## Required Environment Variables

```bash
export MANAGE_SYSTEM_URL="https://<host>"   # API base URL; /v2 is appended automatically
export API_KEY="<token>"                     # Sent as api-key header
export MEMBERSHIP_INVITATION_REDIRECT_URL="https://<your-app>/..." # Required for membership invitation ops unless you pass query param `url`
```

## Running an API Call

From any skill directory:

```bash
python scripts/call_api.py --operation-id OPERATION_ID \
  [--path-params '{"orgId":"..."}'] \
  [--query-params '{"key":"value"}'] \
  [--body '{"field":"value"}'] \
  [--timeout 30]
```

## Architecture

### Skill Directory Layout

```
skills/<skill_name>/
├── SKILL.md          # Defines operations, flow modules, constraints
├── scripts/
│   └── call_api.py   # Thin entry point — delegates to _shared
└── references/
    └── <operation_id>.md   # Full request/response schema per operation
```

### `_shared/` Library

- `manage_system/call_api.py` — CLI entry: parse args → call `run()`
- `manage_system/client.py` — Core HTTP client; reads env vars, renders URL path, calls the API, passes response to metadata extraction
- `manage_system/skill_loader.py` — Parses `SKILL.md`'s `## API Operations` block to extract `method` and `path` for each `### operation_id` heading
- `manage_system/hooks.py` — Per-operation request hooks (e.g. auto-injects redirect URL for membership invitation calls)
- `common/metadata_extraction.py` — Post-response transform: applies `metadata/{operation_id}.json` rules to extract ids and candidate records into Structured Memory

### `metadata/` Directory

Each `{operation_id}.json` file tells `metadata_extraction.py` how to post-process an API response:
- `ids` — scalar key→value extractions stored under `memory.ids`
- `network_candidates` — list extractions stored in named buckets (e.g. `hv_candidates`, `network_candidates`)
- `candidate_limit` — max items retained per bucket (default 20)

Metadata files are resolved first from `<skill_dir>/../metadata/`, then from the repo-root `metadata/` directory.

### How `SKILL.md` Is Parsed

`skill_loader.py` scans the `## API Operations` H2 block. Each `### <operation_id>` H3 section must contain:
- `- method: GET|POST|PATCH|PUT|DELETE`
- `- path: /url/{param}`

These two lines are the only ones required for the HTTP client to function. Everything else (`auth:`, `description:`, parameter tables) is documentation for the AI agent.

### Identifier Resolution Chain

Most operations require canonical IDs obtained in this order:
1. `orgId` — call `get_user_orgs` (skill: `orgs`)
2. `hvId` + `networkId` — call `get_hierarchy_views` (skill: `hvs`)
3. Device `mac` / `network_id` — call `get_inventory` (skill: `orgs`)

Skills explicitly state which prerequisite skills to load in their F0 flow module.

## Skills Overview

| Directory | Purpose |
|-----------|---------|
| `skills/hvs` | Discover hierarchy views and network IDs under an org |
| `skills/networks` | Manage network general settings, ACLs, SSID profiles |
| `skills/network_ap_troubleshoot` | AP real-time diagnostics, device control (ping, speedtest, reboot, upgrade, etc.) |
| `skills/network_switch_troubleshoot` | Switch diagnostics (ping, traceroute, port stats, ARP/FDB) |
| `skills/orgs` | Org management: inventory, licenses, network templates, backups |
| `skills/team_members` | Org/network membership management and invitations |

## Adding a New Skill

1. Create `skills/<skill_name>/SKILL.md` with a `## API Operations` block containing `### <operation_id>` entries with `method:` and `path:` lines.
2. Create `skills/<skill_name>/scripts/call_api.py` copying the two-line pattern from any existing skill's `scripts/call_api.py`.
3. Add `references/<operation_id>.md` for each operation's request/response schema.
4. If the response should populate Structured Memory, add `metadata/{operation_id}.json`.

## Adding a New Operation to an Existing Skill

Add a new `### <operation_id>` block under `## API Operations` in the skill's `SKILL.md`. The block must include `- method:` and `- path:`. Add a matching `references/<operation_id>.md`.
