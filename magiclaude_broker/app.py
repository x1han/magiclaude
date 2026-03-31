from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from magiclaude.schema import ExecuteRequest
from .runner import run_claude_for_request

app = FastAPI(title="magiclaude-broker", version="0.1.0")


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/execute")
def execute(payload: dict):
    try:
        req = ExecuteRequest(**payload)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

    try:
        data = run_claude_for_request(req.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "mode": "remote_mgt",
        "summary": data.get("summary", ""),
        "warnings": data.get("warnings", []),
        "ops": data.get("ops", []),
    }
