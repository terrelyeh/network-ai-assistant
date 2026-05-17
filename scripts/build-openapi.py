#!/usr/bin/env python3
"""Build OpenAPI 3.1 spec from api-skills/skills/*.

Primary source: each skill's SKILL.md `## API Operations` block (the
canonical registry that `_shared/manage_system/skill_loader.py` parses
at runtime).
Supplementary: `references/<op_id>.md` for response examples.

Ops without `- method:` / `- path:` in SKILL.md (RPC, subscribe,
download, hvs.get_hierarchy_views) are marked `x-rd-pending: true`
and placed under `/x-rd-pending/...` so they surface in Swagger UI
as gaps.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import OrderedDict, defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "api-skills" / "skills"
OUTPUT = ROOT / "openapi.json"


# ---------- markdown helpers ----------

def split_table(lines: list[str]) -> list[dict]:
    rows: list[dict] = []
    headers: list[str] = []
    for line in lines:
        s = line.strip()
        if not s.startswith("|"):
            if rows or headers:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not headers:
            headers = [c.lower() for c in cells]
            continue
        if all(re.fullmatch(r"[-: ]*", c) for c in cells):
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def find_json_block(text: str) -> object | None:
    for m in re.finditer(r"```json\s*\n(.+?)\n```", text, re.DOTALL):
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
    return None


# ---------- SKILL.md operations parser ----------

def parse_skill_operations(skill_md: pathlib.Path) -> dict[str, dict]:
    """Parse `## API Operations` block from a SKILL.md."""
    text = skill_md.read_text(encoding="utf-8")
    m = re.search(r"^##\s+API Operations\s*\n(.+?)(?=\n##\s|\Z)", text, re.DOTALL | re.MULTILINE)
    if not m:
        return {}

    block = m.group(1)
    ops: dict[str, dict] = {}
    for chunk in re.split(r"\n###\s+", "\n" + block)[1:]:
        lines = chunk.split("\n")
        op_id = lines[0].strip()
        if not op_id or op_id.startswith("("):
            continue

        meta = {"method": None, "path": None, "auth": None, "description": None}
        i = 1
        while i < len(lines):
            line = lines[i].rstrip()
            if line.startswith("#### "):
                break
            m_kv = re.match(r"^\s*-\s*(method|path|auth|description)\s*:\s*(.+)", line)
            if m_kv:
                key, val = m_kv.group(1), m_kv.group(2).strip()
                if key == "method":
                    meta["method"] = val.upper()
                else:
                    meta[key] = val
            i += 1

        # Parse #### sub-sections (Path Parameters / Query Parameters / Request Body)
        sub_sections: dict[str, list[str]] = {}
        cur: str | None = None
        for line in lines[i:]:
            m_h = re.match(r"^####\s+(.+)", line)
            if m_h:
                cur = m_h.group(1).strip()
                sub_sections.setdefault(cur, [])
                continue
            if cur:
                sub_sections[cur].append(line)

        meta["path_params"] = split_table(sub_sections.get("Path Parameters", []))
        meta["query_params"] = split_table(sub_sections.get("Query Parameters", []))
        meta["body_table"] = split_table(sub_sections.get("Request Body", []))
        ops[op_id] = meta

    return ops


# ---------- reference md parser (supplements SKILL.md) ----------

def parse_reference(md_path: pathlib.Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    lines = text.split("\n")

    description = None
    for line in lines[:6]:
        m = re.match(r"-\s*description:\s*(.+)", line)
        if m:
            description = m.group(1).strip()
            break
    if not description:
        for line in lines[3:]:
            s = line.strip()
            if s and not s.startswith(("-", "#", "|", "`", ">")):
                description = s[:200]
                break

    sections: dict[str, list[str]] = {}
    cur: str | None = None
    for line in lines:
        m = re.match(r"^###\s+(.+)", line)
        if m:
            cur = m.group(1).strip()
            sections.setdefault(cur, [])
            continue
        if cur:
            sections[cur].append(line)

    body_table = split_table(sections.get("Request Body Schema", []))
    if not body_table:
        body_table = split_table(sections.get("Request Body", []))

    request_example = None
    if "Request Body Example" in sections:
        request_example = find_json_block("\n".join(sections["Request Body Example"]))

    response_example = None
    if "Response Body Example" in sections:
        response_example = find_json_block("\n".join(sections["Response Body Example"]))

    return {
        "description": description,
        "body_table": body_table,
        "request_example": request_example,
        "response_example": response_example,
    }


# ---------- schema helpers ----------

MD_TYPE_MAP = {
    "string": "string",
    "str": "string",
    "integer": "integer",
    "int": "integer",
    "number": "number",
    "float": "number",
    "boolean": "boolean",
    "bool": "boolean",
    "array": "array",
    "object": "object",
}


def md_type(t: str) -> str:
    return MD_TYPE_MAP.get((t or "").strip().lower(), "string")


def infer_schema(value: object) -> dict:
    if value is None:
        return {"type": "string", "nullable": True}
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, int):
        return {"type": "integer"}
    if isinstance(value, float):
        return {"type": "number"}
    if isinstance(value, str):
        return {"type": "string"}
    if isinstance(value, list):
        if value:
            return {"type": "array", "items": infer_schema(value[0])}
        return {"type": "array", "items": {}}
    if isinstance(value, dict):
        props = {k: infer_schema(v) for k, v in value.items()}
        return {"type": "object", "properties": props}
    return {}


def build_param(row: dict, location: str) -> dict | None:
    name = row.get("field") or row.get("name")
    if not name or name.startswith("-"):
        return None
    schema = {"type": md_type(row.get("type", "string"))}
    default = row.get("default", "")
    if default and default not in ("-", "—"):
        schema["default"] = default
    param = {
        "name": name,
        "in": location,
        "required": (row.get("required", "").lower() == "true") or (location == "path"),
        "schema": schema,
    }
    if row.get("description"):
        param["description"] = row["description"]
    return param


def build_request_body(rows: list[dict], example: object | None) -> dict | None:
    if not rows and example is None:
        return None
    properties: OrderedDict[str, dict] = OrderedDict()
    required: list[str] = []
    for row in rows:
        name = row.get("field") or row.get("name")
        if not name:
            continue
        prop: dict = {"type": md_type(row.get("type", "string"))}
        if row.get("description"):
            prop["description"] = row["description"]
        properties[name] = prop
        if row.get("required", "").lower() == "true":
            required.append(name)
    schema: dict = {"type": "object"}
    if properties:
        schema["properties"] = dict(properties)
    if required:
        schema["required"] = required
    content: dict = {"schema": schema}
    if example is not None:
        content["example"] = example
    return {"required": bool(required), "content": {"application/json": content}}


# ---------- OpenAPI builder ----------

def op_type_of(op_id: str) -> str:
    if op_id.startswith("rpc_"):
        return "RPC"
    if op_id.startswith("subscribe_"):
        return "SUBSCRIBE"
    if op_id.startswith("download_"):
        return "DOWNLOAD"
    if op_id.startswith("get_"):
        return "READ"
    return "MUTATE"


def build_operation(skill: str, op_id: str, skill_meta: dict, ref_meta: dict) -> dict:
    method = skill_meta.get("method")
    path = skill_meta.get("path")
    description = skill_meta.get("description") or ref_meta.get("description") or op_id
    body_table = skill_meta.get("body_table") or ref_meta.get("body_table") or []

    operation: dict = {
        "operationId": op_id,
        "summary": description[:120],
        "tags": [skill],
        "x-op-type": op_type_of(op_id),
        "x-skill": skill,
    }
    if len(description) > 120:
        operation["description"] = description

    parameters: list[dict] = []
    for row in skill_meta.get("path_params") or []:
        p = build_param(row, "path")
        if p:
            parameters.append(p)
    for row in skill_meta.get("query_params") or []:
        p = build_param(row, "query")
        if p:
            parameters.append(p)
    if parameters:
        operation["parameters"] = parameters

    body = build_request_body(body_table, ref_meta.get("request_example"))
    if body:
        operation["requestBody"] = body

    if ref_meta.get("response_example") is not None:
        operation["responses"] = {
            "200": {
                "description": "Success",
                "content": {
                    "application/json": {
                        "schema": infer_schema(ref_meta["response_example"]),
                        "example": ref_meta["response_example"],
                    }
                },
            }
        }
    else:
        operation["responses"] = {"200": {"description": "Success"}}

    auth = (skill_meta.get("auth") or "").lower()
    if "x-auth-token" in auth:
        operation["security"] = [{"xAuthToken": []}]
    else:
        operation["security"] = [{"apiKeyAuth": []}]

    if not method or not path:
        operation["x-rd-pending"] = (
            "method and path not documented in SKILL.md; awaiting RD answer to "
            "rd-meeting/06-api-doc-questions.md (Q1 for RPC, Q3 for Subscribe, "
            "Q5 for hvs, Q8 for download)."
        )

    return operation


# ---------- main ----------

def main() -> int:
    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").exists())
    if not skill_dirs:
        print(f"ERROR: no skills found under {SKILLS_DIR}", file=sys.stderr)
        return 1

    all_ops: list[tuple[str, str, dict, dict]] = []
    seen: set[tuple[str, str]] = set()
    orphan_refs: list[tuple[str, str]] = []
    skipped_docs: list[tuple[str, str]] = []

    for skill_dir in skill_dirs:
        skill = skill_dir.name
        ops_map = parse_skill_operations(skill_dir / "SKILL.md")
        for op_id, skill_meta in ops_map.items():
            ref_path = skill_dir / "references" / f"{op_id}.md"
            ref_meta = parse_reference(ref_path) if ref_path.exists() else {}
            all_ops.append((skill, op_id, skill_meta, ref_meta))
            seen.add((skill, op_id))

        # Pick up ops that have a reference md but aren't registered in SKILL.md
        for ref_path in (skill_dir / "references").glob("*.md") if (skill_dir / "references").exists() else []:
            op_id = ref_path.stem
            if (skill, op_id) in seen:
                continue
            ref_meta = parse_reference(ref_path)
            # Try to recover method/path from the reference markdown itself
            text = ref_path.read_text(encoding="utf-8")
            m_method = re.search(r"^-\s*method:\s*(\S+)", text, re.MULTILINE)
            m_path = re.search(r"^-\s*path:\s*(\S+)", text, re.MULTILINE)
            has_metadata = bool(m_method or m_path or re.search(r"^-\s*description:", text, re.MULTILINE))
            if not has_metadata:
                skipped_docs.append((skill, op_id))
                continue
            skill_meta: dict = {
                "method": m_method.group(1).upper() if m_method else None,
                "path": m_path.group(1) if m_path else None,
                "auth": None,
                "description": None,
                "path_params": [],
                "query_params": [],
                "body_table": [],
            }
            all_ops.append((skill, op_id, skill_meta, ref_meta))
            orphan_refs.append((skill, op_id))

    skills = sorted({op[0] for op in all_ops})

    spec: dict = {
        "openapi": "3.1.0",
        "info": {
            "title": "EnGenius Cloud AI Agent API",
            "version": "0.1.0",
            "description": (
                "Auto-generated from `api-skills/skills/*/SKILL.md` (canonical "
                "operation registry parsed at runtime by `_shared/manage_system/"
                "skill_loader.py`).\n\n"
                "**Build script**: `scripts/build-openapi.py`.\n\n"
                "**Coverage**: ops with `- method:` and `- path:` in SKILL.md are "
                "fully documented. RPC, Subscribe, and a handful of others are "
                "marked `x-rd-pending` until RD answers `dashboard-builder/docs/"
                "rd-meeting/06-api-doc-questions.md`.\n\n"
                "**Servers**: Falcon (manage system, falcon.<env>.engenius.ai) for "
                "READ/MUT/DL. Dolphin (troubleshoot, dolphin.<env>.engenius.ai) "
                "for RPC/Subscribe — paths TBD."
            ),
            "x-source": "https://github.com/terrelyeh/network-ai-assistant",
        },
        "servers": [
            {
                "url": "https://falcon.staging.engenius.ai/v2",
                "description": "Falcon — manage system API (staging)",
            },
            {
                "url": "https://falcon.dev.engenius.ai/v2",
                "description": "Falcon — manage system API (dev)",
            },
            {
                "url": "https://falcon.production.engenius.ai/v2",
                "description": "Falcon — manage system API (prod)",
            },
            {
                "url": "https://dolphin.staging.engenius.ai",
                "description": "Dolphin — troubleshoot service (staging) — paths TBD",
            },
        ],
        "components": {
            "securitySchemes": {
                "apiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "api-key",
                    "description": "EnGenius Cloud API key — issued per-org.",
                },
                "xAuthToken": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "x-auth-token",
                    "description": "Alternate auth used by `networks` skill ops.",
                },
            }
        },
        "tags": [],
        "paths": {},
    }

    paths: dict[str, dict] = defaultdict(dict)
    counts = {"full": 0, "pending": 0}
    by_type: dict[str, int] = defaultdict(int)

    for skill, op_id, skill_meta, ref_meta in all_ops:
        op = build_operation(skill, op_id, skill_meta, ref_meta)
        if skill_meta.get("method") and skill_meta.get("path"):
            paths[skill_meta["path"]][skill_meta["method"].lower()] = op
            counts["full"] += 1
        else:
            pseudo = f"/x-rd-pending/{skill}/{op_id}"
            paths[pseudo]["post"] = op
            counts["pending"] += 1
        by_type[op_type_of(op_id)] += 1

    op_counts_by_skill: dict[str, int] = defaultdict(int)
    for skill, _, _, _ in all_ops:
        op_counts_by_skill[skill] += 1

    spec["tags"] = [
        {"name": s, "description": f"Skill: {s} ({op_counts_by_skill[s]} ops)"}
        for s in skills
    ]
    spec["paths"] = {k: paths[k] for k in sorted(paths.keys())}

    OUTPUT.write_text(
        json.dumps(spec, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"OK — {OUTPUT.relative_to(ROOT)} written")
    print(f"  Total ops:             {len(all_ops)}")
    print(f"  Fully documented:      {counts['full']}  (method+path resolved)")
    print(f"  x-rd-pending:          {counts['pending']}")
    print(f"  By op_type:            {dict(by_type)}")
    print(f"  Unique HTTP paths:     {sum(1 for k in spec['paths'] if not k.startswith('/x-rd-pending/'))}")
    print(f"  Skills (tags):         {len(skills)}")
    if orphan_refs:
        print(f"  Orphan refs (recovered from reference md): {len(orphan_refs)}")
        for s, o in orphan_refs:
            print(f"    {s}/{o}  -- not registered in SKILL.md, but ref has method/path")
    if skipped_docs:
        print(f"  Non-op doc files (skipped): {len(skipped_docs)}")
        for s, o in skipped_docs:
            print(f"    {s}/{o}.md  -- looks like auxiliary documentation, not an API op")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
