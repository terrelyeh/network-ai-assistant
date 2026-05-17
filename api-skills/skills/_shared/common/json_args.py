from __future__ import annotations

import json
from typing import Any


def parse_json_arg(value: str, name: str, *, require_object: bool) -> Any:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{name} must be valid JSON: {exc}") from exc
    if require_object and not isinstance(parsed, dict):
        raise ValueError(f"{name} must be a JSON object")
    return parsed
