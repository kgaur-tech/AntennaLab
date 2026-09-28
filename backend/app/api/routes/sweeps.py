from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.core.errors import success_response
from backend.app.services.sweep_service import sweep_service

router = APIRouter(prefix="/designs/{design_id}", tags=["sweeps"])


class SweepRequest(BaseModel):
    parameter_path: str = Field(min_length=1)
    start: float
    stop: float
    step: float = Field(gt=0)
    metric: str = Field(min_length=1)


class OptimizationRequest(SweepRequest):
    direction: Literal["maximize", "minimize"] = "maximize"


@router.post("/sweeps")
def run_sweep(design_id: str, request: SweepRequest) -> dict[str, object]:
    return success_response(sweep_service.sweep(design_id, request.parameter_path, request.start, request.stop, request.step, request.metric))


@router.post("/optimizations")
def run_optimization(design_id: str, request: OptimizationRequest) -> dict[str, object]:
    return success_response(sweep_service.optimize(design_id, request.parameter_path, request.start, request.stop, request.step, request.metric, request.direction))
