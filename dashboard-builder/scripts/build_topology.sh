#!/usr/bin/env bash
# Build aggregated multi-org topology JSON
# Calls hvs + org-devices for every org listed in orgs.json,
# captures success/403/402 outcomes per org.

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="/Users/terrelyeh/Downloads/Temp/network-ai-assistant/api-skills"
OUT="$BASE_DIR/live-data/topology.json"

cd "$SKILLS_DIR"
source .venv/bin/activate
export MANAGE_SYSTEM_URL="https://falcon.staging.engenius.ai"
export API_KEY="YWRlNDQ0YjA3NDZlNDI3"

python3 <<'PY'
import json, subprocess, os, datetime, sys
from pathlib import Path

PROTO = Path(os.environ.get("BASE_DIR", "/Users/terrelyeh/Downloads/Temp/network-ai-assistant/.claude/worktrees/exciting-solomon-eb3388/dashboard-builder"))
SKILLS = Path("/Users/terrelyeh/Downloads/Temp/network-ai-assistant/api-skills")

orgs_data = json.loads((PROTO / "live-data/orgs.json").read_text())
orgs = orgs_data["org_candidates"]

def call(skill, op, path_params):
    cmd = [
        "python", str(SKILLS / "skills" / skill / "scripts/call_api.py"),
        "--operation-id", op,
        "--path-params", json.dumps(path_params),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=SKILLS)
    # Strip AAAURL + RequestContext lines from stdout
    out_lines = [l for l in proc.stdout.splitlines() if not l.startswith(("AAAURL", "RequestContext"))]
    out = "\n".join(out_lines).strip()
    if proc.returncode == 0 and out:
        try:
            return {"status": "ok", "data": json.loads(out)}
        except json.JSONDecodeError:
            return {"status": "error", "error": "json_decode_failed", "raw": out[:200]}
    # error path
    err = proc.stderr.strip() or proc.stdout.strip()
    if "HTTP 403" in err:
        return {"status": "forbidden", "error": "Permission Denied (RBAC)"}
    if "HTTP 402" in err:
        return {"status": "payment_required", "error": "PRO plan required"}
    if "HTTP 404" in err:
        return {"status": "not_found", "error": "Not Found"}
    return {"status": "error", "error": err[:200]}

result = {
    "fetched_at": datetime.datetime.now().isoformat(timespec="seconds"),
    "orgs": []
}

for o in orgs:
    print(f"  fetching {o['org_name']}...", file=sys.stderr)
    entry = {
        "org_id": o["org_id"],
        "org_name": o["org_name"],
        "country": o.get("country"),
        "time_zone": o.get("time_zone"),
    }
    hv_res = call("hvs", "get_hierarchy_views", {"orgId": o["org_id"]})
    inv_res = call("org-devices", "get_inventory", {"orgId": o["org_id"]})

    entry["hv_status"] = hv_res["status"]
    entry["inv_status"] = inv_res["status"]

    if hv_res["status"] == "ok":
        entry["hvs"] = hv_res["data"].get("hv_candidates", [])
        entry["networks"] = hv_res["data"].get("network_candidates", [])
    else:
        entry["hv_error"] = hv_res.get("error")
        entry["hvs"] = []
        entry["networks"] = []

    if inv_res["status"] == "ok":
        entry["devices"] = inv_res["data"].get("device_candidates", [])
    else:
        entry["inv_error"] = inv_res.get("error")
        entry["devices"] = []

    result["orgs"].append(entry)

out_path = PROTO / "live-data/topology.json"
out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(f"  wrote {out_path}", file=sys.stderr)
print(f"  {len(result['orgs'])} orgs, {sum(len(o['networks']) for o in result['orgs'])} networks, {sum(len(o['devices']) for o in result['orgs'])} devices total", file=sys.stderr)
PY
