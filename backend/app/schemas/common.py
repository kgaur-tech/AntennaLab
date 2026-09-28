from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ErrorPayload(BaseModel):
    code: str
    message: str
    field: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorPayload


class SuccessResponse(BaseModel):
    success: bool = True
    data: dict[str, Any]
