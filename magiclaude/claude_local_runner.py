from __future__ import annotations

import json
import subprocess
from typing import Any, Dict

from .schema import ExecuteRequest, NotebookOp, ExecuteResponse


SYSTEM_INSTRUCTION = """You are a notebook patch generator.
Return ONLY valid JSON with this schema:
{
  \"summary\": string,
  \"warnings\": string[],
  \"ops\": [
    {\"type\": \"replace_cell\", \"index\": number, \"source\": string, \"cell_type\": \"code\"|\"markdown\"?},
    {\"type\": \"insert_cell_after\", \"index\": number, \"cell_type\": \"code\"|\"markdown\", \"source\": string}
  ]
}
No markdown code fences. No extra text.

Critical source-format rules for every op.source:
1) source MUST NOT contain trigger markers: @c or @n as instruction delimiters
2) source MUST start with exactly these two comment lines:
   # [Requirement]: <brief summary of original user request>
   # [Implementation]: <brief summary of how you implemented it>
3) For replace_cell, output full final cell content only (do not keep original trigger blocks).
"""


def _build_user_payload(req: ExecuteRequest) -> str:
    if req.command == "@c":
        one = req.cells[req.active_cell_index] if req.active_cell_index < len(req.cells) else None
        payload: Dict[str, Any] = {
            "command": req.command,
            "prompt": req.prompt,
            "notebook_path": req.notebook_path,
            "active_cell_index": req.active_cell_index,
            "current_cell": one.model_dump() if one else None,
        }
    else:
        payload = {
            "command": req.command,
            "prompt": req.prompt,
            "notebook_path": req.notebook_path,
            "active_cell_index": req.active_cell_index,
            "cells": [c.model_dump() for c in req.cells],
        }
    return json.dumps(payload, ensure_ascii=False)


def run_local_claude(req: ExecuteRequest, timeout_sec: int = 180, executable_path: str | None = None) -> ExecuteResponse:
    user_payload = _build_user_payload(req)
    exe = (executable_path or "").strip() or "claude"
    cmd = [
        exe,
        "-p",
        f"{SYSTEM_INSTRUCTION}\n\nInput JSON:\n{user_payload}",
    ]
    proc = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
    )
    stdout = (proc.stdout or "").strip()
    data = json.loads(stdout)

    ops = [NotebookOp(**op) for op in data.get("ops", [])]
    return ExecuteResponse(
        mode="local",
        summary=data.get("summary", ""),
        warnings=data.get("warnings", []),
        ops=ops,
    )
