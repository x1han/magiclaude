from __future__ import annotations

import os
from typing import Literal

ModeType = Literal["local", "remote_mgt"]


def resolve_mode_for_user(username: str, requested_mode: str | None = None) -> ModeType:
    if requested_mode in {"local", "remote_mgt"}:
        return requested_mode  # type: ignore[return-value]

    forced = os.getenv("JCM_MODE", "").strip().lower()
    if forced in {"local", "remote_mgt"}:
        return forced  # type: ignore[return-value]

    remote_users = {
        x.strip()
        for x in os.getenv("JCM_REMOTE_USERS", "").split(",")
        if x.strip()
    }
    return "remote_mgt" if username in remote_users else "local"


def resolve_remote_broker_base_url(requested_url: str | None = None) -> str:
    if requested_url and requested_url.strip():
        return requested_url.strip()
    return os.getenv("JCM_REMOTE_BROKER_URL", "http://127.0.0.1:1207")
