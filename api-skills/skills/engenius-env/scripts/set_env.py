#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VALID_ENVS = ("dev", "staging", "prod")
REQUIRED_VARS = (
    "MANAGE_SYSTEM_URL",
    "TROUBLESHOOT_URL",
    "MEMBERSHIP_INVITATION_REDIRECT_URL",
)

_SKILL_DIR = Path(__file__).resolve().parents[1]   # skills/engenius-env/
_OUTPUT_FILE = Path.home() / ".claude" / "engenius_env.json"


def _parse_markdown_table(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if re.fullmatch(r"[-: ]+", cells[0]):   # separator row
            continue
        if cells[0]:
            result[cells[0]] = cells[1]
    return result


def _die(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Write ~/.claude/engenius_env.json for the selected environment."
    )
    parser.add_argument("--env", required=True, choices=VALID_ENVS)
    parser.add_argument("--api-key", required=True, dest="api_key")
    args = parser.parse_args(argv[1:])

    if not args.api_key:
        _die("--api-key must not be empty")

    ref_path = _SKILL_DIR / "reference" / f"{args.env}.md"
    if not ref_path.exists():
        _die(f"Reference file not found: {ref_path}")

    try:
        table = _parse_markdown_table(ref_path.read_text(encoding="utf-8"))
    except OSError as exc:
        _die(f"Cannot read {ref_path}: {exc}")

    missing = [k for k in REQUIRED_VARS if k not in table]
    if missing:
        _die(f"Reference file for '{args.env}' missing: {', '.join(missing)}")

    payload = {k: table[k] for k in REQUIRED_VARS}
    payload["API_KEY"] = args.api_key

    _OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        _OUTPUT_FILE.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        _die(f"Cannot write {_OUTPUT_FILE}: {exc}")

    print(f"Written: {_OUTPUT_FILE}")
    print(f"MANAGE_SYSTEM_URL={payload['MANAGE_SYSTEM_URL']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
