#!/usr/bin/env bash
# sync-refs.sh
#
# Source of truth: dashboard-builder/skill/references/
# Mirror:          api-skills/references/
#
# RD's api-skills package needs its own copy of persona / design.md
# because its SKILL.md MANDATORY-loads them by relative path.
# Run this after editing the source files.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/dashboard-builder/skill/references"
DST="$ROOT/api-skills/references"

if [[ ! -d "$SRC" ]]; then
  echo "ERROR: source not found: $SRC" >&2
  exit 1
fi

if [[ ! -d "$DST" ]]; then
  echo "ERROR: mirror dir not found: $DST" >&2
  echo "       (is api-skills/ vendored?)" >&2
  exit 1
fi

for f in network-admin-persona.md design.md; do
  if [[ ! -f "$SRC/$f" ]]; then
    echo "WARN: source file missing: $SRC/$f — skip" >&2
    continue
  fi
  cp "$SRC/$f" "$DST/$f"
  echo "  synced: $f"
done

# Sync playbooks/ dir (mental-model docs loaded on-demand via persona §3.3)
if [[ -d "$SRC/playbooks" ]]; then
  mkdir -p "$DST/playbooks"
  for f in "$SRC/playbooks"/*.md; do
    [[ -f "$f" ]] || continue
    cp "$f" "$DST/playbooks/$(basename "$f")"
    echo "  synced: playbooks/$(basename "$f")"
  done
fi

echo "done. mirror = $DST"
