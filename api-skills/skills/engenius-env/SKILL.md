---
name: engenius-env
description: >
  Switch the active Engenius API environment (dev / staging / prod).
---

# Engenius Environment Switcher

## Quick Reference

| Task                   | Trigger phrase                          |
| ---------------------- | --------------------------------------- |
| Switch to dev          | "切到 dev" / "use dev" / "test on dev"  |
| Switch to staging      | "切到 staging" / "use staging"          |
| Switch to prod         | "切到 prod" / "use production"          |

## Flow (execute in order)

### Step 1 — Parse target environment

Identify which environment the user wants: `dev`, `staging`, or `prod`.
If the message is ambiguous, default to `dev`.

### Step 2 — Prod confirmation gate

If target is `prod` only: ask "你確定要切換到 **production** 環境？(yes/no)" and stop until user confirms.

### Step 3 — Resolve API key

Check `~/.claude/engenius_env.json` (under the user home directory):
- ask the user: "請輸入 <ENV> 環境的 API Key："
  Wait for the user to provide the key, then use it.

### Step 4 — Run the environment script

Run the following command (substituting ENV from Step 1 and API_KEY from Step 3):

```bash
python skills/engenius-env/scripts/set_env.py --env <ENV> --api-key <API_KEY>
```

- Exit non-zero: report the stderr error to the user verbatim. Do not continue.
- Exit 0: `~/.claude/engenius_env.json` has been written. Proceed to Step 8.


### Step 8 — Report

Read `MANAGE_SYSTEM_URL` from the script's stdout output (line starting with `MANAGE_SYSTEM_URL=`).

Reply with exactly:
```
✓ 已切換到 <ENV> 環境
  MANAGE_SYSTEM_URL = <url>
  API_KEY           = <first-6-chars>…
```

Do not ask any further questions. The user can now run any skill directly.

## Constraints

- C1 Never display the full `API_KEY`. Show only the first 6 characters followed by `…`.
