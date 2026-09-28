from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.core.errors import success_response
from backend.app.services.analysis_service import analysis_service

router = APIRouter(tags=["analysis"])


class AnalysisRequest(BaseModel):
    settings: dict[str, Any] = Field(default_factory=dict)


@router.post("/designs/{design_id}/analysis")
def run_analysis(design_id: str, request: AnalysisRequest) -> dict[str, object]:
    return success_response(analysis_service.analyze(design_id, request.settings))


@router.get("/designs/{design_id}/analysis")
def get_latest_analysis(design_id: str) -> dict[str, object]:
    result = analysis_service.latest(design_id)
    return success_response({"analysis": result, "status": "READY" if result is None else "COMPLETED"})


@router.get("/analysis/{analysis_id}")
def get_analysis(analysis_id: str) -> dict[str, object]:
    return success_response(analysis_service.get(analysis_id))
