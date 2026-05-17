from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def transform_response_with_metadata(
    *,
    data: Any,
    operation_id: str,
    path_params: dict[str, Any] | None = None,
    skill_dir: Path | None = None,
) -> Any:
    spec = _load_metadata_spec(operation_id, skill_dir=skill_dir)
    if not spec:
        return data

    memory = _initial_memory_from_path_params(path_params or {})
    return _apply_metadata_extraction(spec=spec, data=data, memory=memory)


def _skills_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_metadata_spec(operation_id: str, *, skill_dir: Path | None) -> dict[str, Any] | None:
    candidates: list[Path] = []
    if skill_dir is not None:
        candidates.append(skill_dir.parent / "metadata" / f"{operation_id}.json")
    candidates.append(_skills_root() / "metadata" / f"{operation_id}.json")

    seen: set[Path] = set()
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    return None


def _apply_metadata_extraction(*, spec: dict[str, Any], data: Any, memory: dict[str, Any]) -> dict[str, Any]:
    for bucket in spec.get("clear_buckets_before_extract", []):
        if bucket and bucket != "ids":
            memory.pop(bucket, None)

    ids = dict(memory.get("ids", {}))
    candidate_rules = list(spec.get("network_candidates", []))
    candidate_buckets: dict[str, list[dict[str, Any]]] = {}
    for rule in candidate_rules:
        bucket = rule.get("target_bucket") or "network_candidates"
        candidate_buckets[bucket] = list(memory.get(bucket, []))

    for rule in spec.get("ids", []):
        _apply_id_rule(rule=rule, data=data, ids=ids)
    for rule in candidate_rules:
        bucket = rule.get("target_bucket") or "network_candidates"
        _apply_candidate_rule(rule=rule, data=data, ids=ids, candidates=candidate_buckets[bucket])

    if ids:
        memory["ids"] = ids
    limit = int(spec.get("candidate_limit") or 20)
    for bucket, values in candidate_buckets.items():
        memory[bucket] = values[-limit:]
    return memory


def _apply_id_rule(*, rule: dict[str, Any], data: Any, ids: dict[str, str]) -> None:
    values: list[str] = []
    for node in _select_nodes(data, str(rule.get("source_path") or "$")):
        if not isinstance(node, dict):
            continue
        if not _has_required_fields(node, list(rule.get("required_fields") or [])):
            continue
        value = node.get(str(rule.get("value_field") or ""))
        if value is not None:
            values.append(str(value))
    if not values:
        return
    memory_key = str(rule.get("memory_key") or "")
    if memory_key:
        ids[memory_key] = values[0] if rule.get("take", "first") == "first" else values[-1]


def _apply_candidate_rule(
    *,
    rule: dict[str, Any],
    data: Any,
    ids: dict[str, str],
    candidates: list[dict[str, Any]],
) -> None:
    replace_scope_field = str(rule.get("replace_scope_field") or "")
    replace_scope_source = str(rule.get("replace_scope_value_source") or "")
    if replace_scope_field and replace_scope_source:
        scope_value = _resolve_scope_value(source=replace_scope_source, ids=ids)
        if scope_value not in (None, ""):
            scope_text = str(scope_value)
            candidates[:] = [item for item in candidates if str(item.get(replace_scope_field, "")) != scope_text]

    for node in _select_nodes(data, str(rule.get("source_path") or "$")):
        if not isinstance(node, dict):
            continue
        if not _has_required_fields(node, list(rule.get("required_fields") or [])):
            continue
        candidate: dict[str, Any] = {}
        for out_key, source_key in dict(rule.get("field_map") or {}).items():
            value = _resolve_source_value(node=node, source_key=str(source_key), ids=ids)
            if value is not None:
                candidate[str(out_key)] = value
        for out_key, default_value in dict(rule.get("defaults") or {}).items():
            if str(out_key) not in candidate and isinstance(default_value, str):
                if default_value.startswith("$memory.ids."):
                    candidate[str(out_key)] = ids.get(default_value.removeprefix("$memory.ids."), "")
        required_out = str(rule.get("required_output_field") or "network_id")
        if required_out and not candidate.get(required_out):
            continue
        if candidate not in candidates:
            candidates.append(candidate)


def _resolve_scope_value(*, source: str, ids: dict[str, str]) -> Any:
    if source.startswith("$memory.ids."):
        return ids.get(source.removeprefix("$memory.ids."))
    return source


def _resolve_source_value(*, node: dict[str, Any], source_key: str, ids: dict[str, str]) -> Any:
    if source_key.startswith("$memory.ids."):
        return ids.get(source_key.removeprefix("$memory.ids."))
    return _get_by_dotted_key(node, source_key)


def _get_by_dotted_key(node: dict[str, Any], dotted_key: str) -> Any:
    current: Any = node
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current.get(part)
    return current


def _has_required_fields(node: dict[str, Any], required_fields: list[str]) -> bool:
    return all(node.get(field) is not None for field in required_fields)


def _select_nodes(value: Any, path: str) -> list[Any]:
    if not path or path == "$":
        return [value]

    tokens = [part for part in path.removeprefix("$.").split(".") if part]
    nodes: list[Any] = [value]
    for token in tokens:
        next_nodes: list[Any] = []
        for node in nodes:
            if token == "*":
                if isinstance(node, list):
                    next_nodes.extend(node)
                elif isinstance(node, dict):
                    next_nodes.extend(node.values())
                continue
            if isinstance(node, dict) and token in node:
                next_nodes.append(node[token])
        nodes = next_nodes
        if not nodes:
            break
    return nodes


def _initial_memory_from_path_params(path_params: dict[str, Any]) -> dict[str, Any]:
    ids: dict[str, str] = {}
    path_param_map = {
        "orgId": "org_id",
        "hvId": "hv_id",
        "networkId": "network_id",
        "userId": "user_id",
        "deviceId": "device_id",
        "backupId": "backup_id",
        "templateId": "template_id",
        "groupId": "group_id",
        "clientMac": "mac",
        "licenseKey": "license_key",
    }
    for param_name, value in path_params.items():
        if value in (None, ""):
            continue
        memory_key = path_param_map.get(param_name)
        if memory_key:
            ids[memory_key] = str(value)
    if "hv_id" in ids:
        ids.setdefault("hierarchy_view_id", ids["hv_id"])
    return {"ids": ids} if ids else {}
