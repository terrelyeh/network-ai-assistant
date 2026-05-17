from __future__ import annotations

import json
import os
from pathlib import Path

_ENV_JSON = Path.home() / ".claude" / "engenius_env.json"

def _load_env_json() -> dict:
    try:
        if _ENV_JSON.exists():
            return json.loads(_ENV_JSON.read_text())
    except Exception:
        pass
    return {}


def required_env(name: str) -> str:
    env_override = _load_env_json()
    value = env_override.get(name, "").strip() if name in env_override else os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"{name} environment variable required")
    return value
