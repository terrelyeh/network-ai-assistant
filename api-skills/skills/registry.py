from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class ParameterSpec(BaseModel):
    name: str
    param_type: str
    required: bool
    default: Any | None = None
    description: str = ""


class ApiOperationSpec(BaseModel):
    operation_id: str
    method: str
    path: str
    description: str = ""
    summary: str = ""
    auth_type: str = "none"
    auth_header_name: str | None = None
    static_headers: dict[str, str] = Field(default_factory=dict)
    path_params: list[ParameterSpec] = Field(default_factory=list)
    query_params: list[ParameterSpec] = Field(default_factory=list)
    body_params: list[ParameterSpec] = Field(default_factory=list)


class SkillSummary(BaseModel):
    id: str
    name: str
    description: str


class SkillDetail(BaseModel):
    name: str
    description: str
    instructions: str
    operations: list[ApiOperationSpec] = Field(default_factory=list)
    base_dir: Path


class SkillRegistry:
    _cache: dict[str, SkillDetail] = {}

    @classmethod
    def _skills_root(cls) -> Path:
        return Path(__file__).resolve().parent

    @classmethod
    def _skill_dirs(cls) -> list[Path]:
        dirs: list[Path] = []
        for child in cls._skills_root().iterdir():
            if not child.is_dir() or child.name.startswith("_"):
                continue
            if (child / "SKILL.md").exists():
                dirs.append(child)
        return sorted(dirs, key=lambda p: p.name)

    @classmethod
    def list_summaries(cls) -> list[SkillSummary]:
        out: list[SkillSummary] = []
        for skill_dir in cls._skill_dirs():
            meta, _, _ = _parse_skill_md((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
            name = str(meta.get("name", skill_dir.name))
            out.append(SkillSummary(id=name, name=name, description=str(meta.get("description", "")).strip()))
        return out

    @classmethod
    def get_skill(cls, skill_name: str) -> SkillDetail:
        if skill_name in cls._cache:
            return cls._cache[skill_name]

        skill_dir = cls._skills_root() / skill_name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            raise ValueError(f"Skill not found: {skill_name}")

        meta, body, parts = _parse_skill_md(skill_md.read_text(encoding="utf-8"))
        detail = SkillDetail(
            name=str(meta.get("name", skill_name)),
            description=str(meta.get("description", "")).strip(),
            instructions=body.strip(),
            operations=_parse_api_operations(
                parts.get("API Operations", ""),
                reference_body_params=_load_reference_request_body_params(skill_dir),
            ),
            base_dir=skill_dir,
        )
        cls._cache[skill_name] = detail
        return detail

    @classmethod
    def get_api_operations(cls, skill_name: str) -> list[ApiOperationSpec]:
        return cls.get_skill(skill_name).operations

    @classmethod
    def get_api_operation(cls, skill_name: str, operation_id: str) -> ApiOperationSpec | None:
        for op in cls.get_api_operations(skill_name):
            if op.operation_id == operation_id:
                return op
        return None

    @classmethod
    def find_operation_in_selected(
        cls, selected_skills: list[str], operation_id: str
    ) -> tuple[str | None, ApiOperationSpec | None]:
        for skill in selected_skills:
            op = cls.get_api_operation(skill, operation_id)
            if op is not None:
                return skill, op
        return None, None

    @classmethod
    def find_operation_anywhere(cls, operation_id: str) -> str | None:
        """Scan every known skill for the operation and return the owning
        skill's name, regardless of whether it is currently selected. Used
        by the executor to distinguish 'skill_not_loaded' from
        'operation_not_found' when the router fails to resolve.
        """
        if not operation_id:
            return None
        for skill_dir in cls._skill_dirs():
            skill_name = skill_dir.name
            try:
                op = cls.get_api_operation(skill_name, operation_id)
            except Exception:
                continue
            if op is not None:
                return skill_name
        return None

    @classmethod
    def find_all_skills_with_operation(
        cls, selected_skills: list[str], operation_id: str
    ) -> list[str]:
        return [
            skill for skill in selected_skills
            if cls.get_api_operation(skill, operation_id) is not None
        ]

    @classmethod
    def known_skill_names(cls) -> set[str]:
        return {p.name for p in cls._skill_dirs()}

    @classmethod
    def read_reference(cls, skill_name: str, filename: str) -> str:
        target = cls._skills_root() / skill_name / "references" / filename
        if not target.exists():
            raise ValueError(f"Reference not found: {skill_name}/references/{filename}")
        return target.read_text(encoding="utf-8")


def _parse_skill_md(content: str) -> tuple[dict[str, Any], str, dict[str, str]]:
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", content, flags=re.S)
    if not match:
        raise ValueError("SKILL.md missing YAML front matter")
    meta_raw, body = match.groups()
    meta = yaml.safe_load(meta_raw) or {}
    parts = _split_h2_sections(body)
    return meta, body, parts


def _split_h2_sections(body: str) -> dict[str, str]:
    pieces = re.split(r"\n##\s+", "\n" + body)
    out: dict[str, str] = {}
    for piece in pieces[1:]:
        lines = piece.splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        out[title] = "\n".join(lines[1:]).strip()
    return out



def _parse_api_operations(
    block: str,
    reference_body_params: dict[str, list[ParameterSpec]] | None = None,
) -> list[ApiOperationSpec]:
    if not block.strip():
        return []
    reference_body_params = reference_body_params or {}
    chunks = re.split(r"\n###\s+", "\n" + block)
    operations: list[ApiOperationSpec] = []
    for chunk in chunks[1:]:
        lines = [x.rstrip() for x in chunk.splitlines()]
        if not lines:
            continue
        operation_id = lines[0].strip()
        method = "GET"
        path = "/"
        description = ""
        summary = ""
        auth_type = "none"
        auth_header_name: str | None = None

        for line in lines[1:]:
            value = line.strip().lstrip("- ").strip()
            if value.startswith("method:"):
                method = value.split(":", 1)[1].strip().upper()
            elif value.startswith("path:"):
                path = value.split(":", 1)[1].strip()
            elif value.startswith("description:"):
                description = value.split(":", 1)[1].strip()
            elif value.startswith("summary:"):
                summary = value.split(":", 1)[1].strip()
            elif value.startswith("auth:"):
                hint = value.split(":", 1)[1].strip().lower()
                if "bearer" in hint:
                    auth_type = "bearer"
                elif "x-auth-token" in hint or "api key" in hint:
                    auth_type = "api_key"
                    auth_header_name = "x-auth-token"
                elif "basic" in hint:
                    auth_type = "basic"
                else:
                    auth_type = "none"

        path_params = _parse_param_table(chunk, "Path Parameters")
        query_params = _parse_param_table(chunk, "Query Parameters")
        body_params = _parse_param_table(chunk, "Request Body")
        if not body_params:
            body_params = [
                spec.model_copy()
                for spec in reference_body_params.get(operation_id, [])
            ]

        operations.append(
            ApiOperationSpec(
                operation_id=operation_id,
                method=method,
                path=path,
                description=description,
                summary=summary or description or operation_id,
                auth_type=auth_type,
                auth_header_name=auth_header_name,
                path_params=path_params,
                query_params=query_params,
                body_params=body_params,
            )
        )
    return operations


def _load_reference_request_body_params(skill_dir: Path) -> dict[str, list[ParameterSpec]]:
    refs_dir = skill_dir / "references"
    if not refs_dir.exists():
        return {}

    out: dict[str, list[ParameterSpec]] = {}
    for md_file in refs_dir.glob("*.md"):
        operation_id = md_file.stem
        content = md_file.read_text(encoding="utf-8")
        body_params = _parse_reference_request_body_params(content)
        if body_params:
            out[operation_id] = body_params
    return out


def _parse_reference_request_body_params(section_text: str) -> list[ParameterSpec]:
    for section_name in ("Request Body Schema", "Request Body Item Schema", "Request Body"):
        specs = _parse_reference_param_table(section_text, section_name)
        if specs:
            return specs
    return []


def _parse_reference_param_table(section_text: str, section_name: str) -> list[ParameterSpec]:
    m = re.search(
        rf"###\s+{re.escape(section_name)}\n(.*?)(?:\n###|\n##|\Z)",
        section_text,
        flags=re.S,
    )
    if not m:
        return []
    text = m.group(1).strip()
    rows = [line.strip() for line in text.splitlines() if line.strip().startswith("|")]
    if len(rows) < 3:
        return []

    header = [h.strip().lower() for h in rows[0].strip("|").split("|")]
    name_key = "field" if "field" in header else "name" if "name" in header else None
    if not name_key or "type" not in header:
        return []

    specs: list[ParameterSpec] = []
    for row in rows[2:]:
        cols = [c.strip() for c in row.strip("|").split("|")]
        if len(cols) != len(header):
            continue
        data = dict(zip(header, cols))
        name = data.get(name_key, "")
        if not name:
            continue
        required_text = data.get("required", "false").lower()
        required = required_text in {"true", "yes", "1", "required"}
        specs.append(
            ParameterSpec(
                name=name,
                param_type=data.get("type", "string").strip().lower(),
                required=required,
                default=None,
                description=data.get("description", ""),
            )
        )
    return specs


def _parse_param_table(operation_chunk: str, section_name: str) -> list[ParameterSpec]:
    m = re.search(rf"####\s+{re.escape(section_name)}\n(.*?)(?:\n####|\n###|\Z)", operation_chunk, flags=re.S)
    if not m:
        return []
    text = m.group(1).strip()
    if not text or "(EMPTY)" in text or "(none)" in text.lower():
        return []
    rows = [line.strip() for line in text.splitlines() if line.strip().startswith("|")]
    if len(rows) < 3:
        return []
    header = [h.strip().lower() for h in rows[0].strip("|").split("|")]
    specs: list[ParameterSpec] = []
    for row in rows[2:]:
        cols = [c.strip() for c in row.strip("|").split("|")]
        if len(cols) != len(header):
            continue
        data = dict(zip(header, cols))
        name = data.get("name", "")
        if not name:
            continue
        required_text = data.get("required", "false").lower()
        required = required_text in {"true", "yes", "1", "required"}
        default = data.get("default")
        if default in {"", "null", "none", None}:
            default = None
        param_type = data.get("type", "string").strip().lower()
        specs.append(
            ParameterSpec(
                name=name,
                param_type=param_type,
                required=required,
                default=default,
                description=data.get("description", ""),
            )
        )
    return specs
