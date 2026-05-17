from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

MEMBERSHIP_INVITATION_REDIRECT_URL_ENV = "MEMBERSHIP_INVITATION_REDIRECT_URL"
DEFAULT_MEMBERSHIP_INVITATION_REDIRECT_URL = "https://lark.dev.engenius.ai/dlink/cloud2go"


@dataclass
class RequestContext:
    operation_id: str
    skill_dir: Path
    operation: dict[str, str]
    path_params: dict[str, Any]
    query_params: dict[str, Any]
    body: Any
    headers: dict[str, str]


RequestHook = Callable[[RequestContext], None]


def apply_request_hooks(context: RequestContext) -> None:
    for hook in REQUEST_HOOKS.get("*", []):
        hook(context)
    for hook in REQUEST_HOOKS.get(context.operation_id, []):
        hook(context)


def _apply_membership_invitation_redirect_url(context: RequestContext) -> None:
    if context.query_params.get("url"):
        return
    context.query_params["url"] = (os.environ.get(MEMBERSHIP_INVITATION_REDIRECT_URL_ENV, "").strip() or DEFAULT_MEMBERSHIP_INVITATION_REDIRECT_URL)


REQUEST_HOOKS: dict[str, list[RequestHook]] = {
    "create_org_memberships": [_apply_membership_invitation_redirect_url],
    "patch_networks_memberships": [_apply_membership_invitation_redirect_url],
    "create_org_member_user_invitation": [_apply_membership_invitation_redirect_url],
}
