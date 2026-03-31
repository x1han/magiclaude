from __future__ import annotations

from typing import Literal, Optional, List
from pydantic import BaseModel, Field, field_validator, model_validator

OpType = Literal["replace_cell", "insert_cell_after"]
CellType = Literal["code", "markdown"]
ModeType = Literal["local", "remote_mgt"]


class CellPayload(BaseModel):
    cell_type: CellType
    source: str


class NotebookOp(BaseModel):
    type: OpType
    index: int = Field(ge=0)
    cell_type: Optional[CellType] = None
    source: str = ""

    @model_validator(mode="after")
    def validate_by_type(self):
        if self.type == "insert_cell_after" and self.cell_type is None:
            raise ValueError("insert_cell_after requires cell_type")
        return self


class ExecuteRequest(BaseModel):
    command: Literal["@c", "@n"]
    prompt: str = Field(min_length=1, max_length=10000)
    notebook_path: str
    active_cell_index: int = Field(ge=0)
    cells: List[CellPayload] = Field(default_factory=list)
    dry_run: bool = True
    claude_executable_path: Optional[str] = Field(default=None, max_length=2048)
    jcm_mode: Optional[ModeType] = None
    remote_broker_url: Optional[str] = Field(default=None, max_length=2048)

    @field_validator("cells")
    @classmethod
    def validate_cells_length(cls, v: List[CellPayload]):
        if len(v) > 500:
            raise ValueError("too many cells, max=500")
        return v


class ExecuteResponse(BaseModel):
    mode: ModeType
    summary: str = ""
    warnings: List[str] = Field(default_factory=list)
    ops: List[NotebookOp] = Field(default_factory=list)
