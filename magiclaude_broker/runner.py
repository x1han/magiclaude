from __future__ import annotations

import json
import subprocess

SYSTEM_INSTRUCTION = """You are a notebook patch generator.
Return ONLY valid JSON with schema:
{\"summary\": string, \"warnings\": string[], \"ops\": [{...}]}
No markdown fences.
"""


def run_claude_for_request(payload: dict, timeout_sec: int = 180) -> dict:
    cmd = [
        "claude",
        "-p",
        f"{SYSTEM_INSTRUCTION}\n\nInput JSON:\n{json.dumps(payload, ensure_ascii=False)}",
    ]
    proc = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
    )
    return json.loads((proc.stdout or "").strip())
