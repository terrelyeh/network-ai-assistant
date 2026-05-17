from __future__ import annotations

import re
from typing import Any
from urllib.parse import quote

import requests

from ..common.env import required_env
from ..common.metadata_extraction import transform_response_with_metadata
from .hooks import RequestContext, apply_request_hooks
from .skill_loader import get_operation, resolve_skill_dir

BASE_URL_ENV = "MANAGE_SYSTEM_URL"
API_KEY_ENV = "API_KEY"


def run(
    *,
    operation_id: str,
    path_params: dict[str, Any],
    query_params: dict[str, Any],
    body: Any,
    extra_headers: dict[str, Any],
    timeout: int,
    skill_name: str | None = None,
) -> Any:
    base_url = required_env(BASE_URL_ENV)
    api_key = required_env(API_KEY_ENV)
    skill_dir = resolve_skill_dir(skill_name)
    operation = get_operation(skill_dir=skill_dir, operation_id=operation_id)

    context = RequestContext(
        operation_id=operation_id,
        skill_dir=skill_dir,
        operation=operation,
        path_params=dict(path_params or {}),
        query_params=dict(query_params or {}),
        body=body,
        headers=build_headers(api_key=api_key, extra_headers=extra_headers),
    )
    apply_request_hooks(context)

    path = render_path(context.operation["path"], context.path_params)
    url = build_api_url(base_url=base_url, path=path)
    print("AAAURL", url)
    print(context)

    resp = requests.request(
        context.operation["method"],
        url,
        headers=context.headers,
        params=context.query_params,
        json=context.body if context.operation["method"] in {"POST", "PUT", "PATCH", "DELETE"} else None,
        timeout=timeout,
    )
    resp.raise_for_status()
    data = resp.json()
    return transform_response_with_metadata(
        data=data,
        operation_id=operation_id,
        path_params=context.path_params,
        skill_dir=skill_dir,
    )


def render_path(template: str, path_params: dict[str, Any]) -> str:

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in path_params or path_params[key] in (None, ""):
            raise ValueError(f"Missing required path param '{key}'")
        return quote(str(path_params[key]), safe="")

    return re.sub(r"\{([^{}]+)\}", replace, template)


def build_headers(*, api_key: str, extra_headers: dict[str, Any]) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    headers.update({str(k): str(v) for k, v in (extra_headers or {}).items()})
    headers["api-key"] = api_key
    return headers


def build_api_url(*, base_url: str, path: str) -> str:
    root = base_url.rstrip("/")
    if not root.endswith("/v2"):
        root = f"{root}/v2"
    return f"{root}{path if path.startswith('/') else '/' + path}"


_build_api_url = build_api_url
