#!/usr/bin/env bash
# refresh-all.sh — Pre-demo data refresh
# Pulls all 6 live-data/*.json + topology.json from real staging API.
# Run this 2-5 minutes before a booth demo so the dashboards show live data.

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROTO_DIR="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="/Users/terrelyeh/Downloads/Temp/network-ai-assistant/api-skills"
LIVE="$PROTO_DIR/live-data"

mkdir -p "$LIVE"

# --- Setup ---
cd "$SKILLS_DIR"
source .venv/bin/activate
export MANAGE_SYSTEM_URL="${MANAGE_SYSTEM_URL:-https://falcon.staging.engenius.ai}"
export API_KEY="${API_KEY:-YWRlNDQ0YjA3NDZlNDI3}"

# Org IDs (resolved from get_user_orgs; could re-resolve but we know them)
MAIN_ORG="5e410f44e91984972fd50a22"
VERTICAL_ORG="671a1fa12103d1fdf8485781"

# Suppress AAAURL/RequestContext debug lines that the skill prints
clean() { grep -v "^AAAURL" | grep -v "^RequestContext"; }

# --- Pretty printer ---
GRN='\033[0;32m'; YEL='\033[1;33m'; RED='\033[0;31m'; DIM='\033[2m'; NC='\033[0m'
ok()    { echo -e "  ${GRN}✓${NC} $1"; }
warn()  { echo -e "  ${YEL}⚠${NC} $1"; }
fail()  { echo -e "  ${RED}✗${NC} $1"; }
title() { echo -e "${DIM}===${NC} $1 ${DIM}===${NC}"; }

START=$(date +%s)

# --- 1. Orgs ---
title "orgs"
if python skills/init-orgs/scripts/call_api.py --operation-id get_user_orgs 2>/dev/null | clean > "$LIVE/orgs.json"; then
  COUNT=$(python3 -c "import json; print(len(json.load(open('$LIVE/orgs.json')).get('org_candidates',[])))")
  ok "orgs.json ($COUNT orgs)"
else
  fail "get_user_orgs failed"
fi

# --- 2. Hierarchy (Main_Org — primary dashboard target) ---
title "hierarchy + inventory (Main_Org)"
if python skills/hvs/scripts/call_api.py --operation-id get_hierarchy_views \
    --path-params "{\"orgId\":\"$MAIN_ORG\"}" 2>/dev/null | clean > "$LIVE/hierarchy.json"; then
  COUNT=$(python3 -c "import json; print(len(json.load(open('$LIVE/hierarchy.json')).get('network_candidates',[])))")
  ok "hierarchy.json ($COUNT networks in Main_Org)"
else
  fail "get_hierarchy_views Main_Org failed"
fi

# --- 3. Inventory (Main_Org) ---
if python skills/org-devices/scripts/call_api.py --operation-id get_inventory \
    --path-params "{\"orgId\":\"$MAIN_ORG\"}" 2>/dev/null | clean > "$LIVE/inventory.json"; then
  COUNT=$(python3 -c "import json; print(len(json.load(open('$LIVE/inventory.json')).get('device_candidates',[])))")
  ok "inventory.json ($COUNT devices in Main_Org)"
else
  fail "get_inventory Main_Org failed"
fi

# --- 4. Licenses (Main_Org) ---
title "licenses + members"
if python skills/org-licenses/scripts/call_api.py --operation-id get_licenses \
    --path-params "{\"orgId\":\"$MAIN_ORG\"}" 2>/dev/null | clean > "$LIVE/licenses.json"; then
  COUNT=$(python3 -c "import json; print(len(json.load(open('$LIVE/licenses.json')).get('license_candidates',[])))")
  ok "licenses.json ($COUNT in pool)"
else
  fail "get_licenses Main_Org failed"
fi

# --- 5. Members (Main_Org) ---
if python skills/team-members/scripts/call_api.py --operation-id get_org_memberships_overall \
    --path-params "{\"orgId\":\"$MAIN_ORG\"}" 2>/dev/null | clean > "$LIVE/memberships.json"; then
  COUNT=$(python3 -c "
import json; from datetime import datetime
m=json.load(open('$LIVE/memberships.json'))
all=m.get('org_member_candidates',[])
stale=[x for x in all if x.get('last_login_time',0) and (datetime.now().timestamp()*1000 - x['last_login_time'])/86400000 > 365]
print(f'{len(all)} members, {len(stale)} stale (1y+)')
")
  ok "memberships.json ($COUNT)"
else
  fail "get_org_memberships_overall Main_Org failed"
fi

# --- 6. Topology (cross-org aggregate) ---
title "topology (cross-org)"
# Delegate to existing build script which handles 5 orgs
if [ -x "$SCRIPT_DIR/build_topology.sh" ]; then
  PROTO_DIR="$PROTO_DIR" bash "$SCRIPT_DIR/build_topology.sh" >/dev/null 2>&1
  if [ -f "$LIVE/topology.json" ]; then
    SUMMARY=$(python3 -c "
import json
t=json.load(open('$LIVE/topology.json'))
orgs=t.get('orgs',[])
nets=sum(len(o.get('networks',[])) for o in orgs)
devs=sum(len(o.get('devices',[])) for o in orgs)
acc=sum(1 for o in orgs if o.get('hv_status')=='ok' and o.get('inv_status')=='ok')
print(f'{acc}/{len(orgs)} orgs accessible, {nets} networks, {devs} devices')
")
    ok "topology.json ($SUMMARY)"
  else
    fail "topology.json missing"
  fi
else
  warn "build_topology.sh not executable; skipping topology refresh"
fi

# --- Summary ---
END=$(date +%s)
ELAPSED=$((END - START))
echo ""
title "summary"
echo -e "  ${GRN}refresh complete in ${ELAPSED}s${NC}"
echo -e "  ${DIM}live-data/${NC}"
ls -lh "$LIVE"/*.json 2>/dev/null | awk '{print "    " $9 "  " $5 "  " $6 " " $7 " " $8}'

# Tip
echo ""
echo -e "${DIM}Next:${NC}  open http://localhost:8765/architecture-demo.html"
echo -e "${DIM}      ${NC}  or compose any spec:"
echo -e "${DIM}      ${NC}  python prototype/dashboard-builder-skill/scripts/compose.py --spec <spec.json> --out <out.html>"
