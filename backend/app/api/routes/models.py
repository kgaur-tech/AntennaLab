from __future__ import annotations

from fastapi import APIRouter

from backend.app.core.errors import success_response
from backend.app.services.model_registry import model_registry

router = APIRouter(prefix="/models", tags=["models"])


@router.get("")
def list_models() -> dict[str, object]:
    return success_response({"models": model_registry.list_models()})
