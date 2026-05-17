from __future__ import annotations

import re
import sys
from pathlib import Path


def resolve_skill_dir(skill_name: str | None = None) -> Path:
    skills_root = _skills_root()
    if skill_name:
        skill_dir = skills_root / skill_name
        if (skill_dir / "SKILL.md").exists():
            return skill_dir
        raise ValueError(f"Skill not found: {skill_name}")

    inferred = _infer_skill_dir_from_argv()
    if inferred is not None:
        return inferred

    raise ValueError("Cannot infer skill directory. Run this script via skills/<name>/scripts/call_api.py.")


def get_operation(*, skill_dir: Path, operation_id: str) -> dict[str, str]:
    operations = parse_skill_operations(skill_dir / "SKILL.md")
    operation = operations.get(operation_id)
    if operation is None:
        raise ValueError(f"Operation '{operation_id}' not found in {skill_dir.name}/SKILL.md")
    return operation


def _skills_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _infer_skill_dir_from_argv() -> Path | None:
    try:
        script_path = Path(sys.argv[0]).resolve()
    except OSError:
        return None
    for parent in script_path.parents:
        if parent.parent.name == "skills" and (parent / "SKILL.md").exists():
            return parent
    return None


def parse_skill_operations(skill_md: Path) -> dict[str, dict[str, str]]:
    content = skill_md.read_text(encoding="utf-8")
    api_block = _extract_h2_block(content, "API Operations")
    operations: dict[str, dict[str, str]] = {}
    for chunk in re.split(r"\n###\s+", "\n" + api_block)[1:]:
        lines = [line.rstrip() for line in chunk.splitlines()]
        if not lines:
            continue
        operation_id = lines[0].strip()
        method = ""
        path = ""
        for line in lines[1:]:
            value = line.strip().lstrip("- ").strip()
            if value.startswith("method:"):
                method = value.split(":", 1)[1].strip().upper()
            elif value.startswith("path:"):
                path = value.split(":", 1)[1].strip()
        if operation_id and method and path:
            operations[operation_id] = {"method": method, "path": path}
    return operations


def _extract_h2_block(content: str, title: str) -> str:
    match = re.search(rf"^##\s+{re.escape(title)}\s*$", content, flags=re.M)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^##\s+", content[start:], flags=re.M)
    end = start + next_match.start() if next_match else len(content)
    return content[start:end].strip()
