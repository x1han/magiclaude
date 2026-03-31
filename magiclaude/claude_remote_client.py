from __future__ import annotations

import httpx

from .schema import ExecuteRequest, ExecuteResponse, NotebookOp
from .routing import resolve_remote_broker_base_url


def run_remote_claude(req: ExecuteRequest, timeout_sec: int = 180, remote_broker_url: str | None = None) -> ExecuteResponse:
    url = resolve_remote_broker_base_url(remote_broker_url).rstrip("/") + "/execute"
    with httpx.Client(timeout=timeout_sec) as client:
        resp = client.post(url, json=req.model_dump())
        resp.raise_for_status()
        data = resp.json()

    ops = [NotebookOp(**op) for op in data.get("ops", [])]
    return ExecuteResponse(
        mode="remote_mgt",
        summary=data.get("summary", ""),
        warnings=data.get("warnings", []),
        ops=ops,
    )
