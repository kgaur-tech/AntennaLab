from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from backend.app.core.errors import success_response
from backend.app.schemas.design_schema import DesignCreateRequest
from backend.app.services.design_service import DesignService
from backend.app.services.model_registry import model_registry

router = APIRouter(prefix="/designs", tags=["designs"])


class DesignUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    parameters: dict[str, Any]


@router.get("/families")
def list_supported_families() -> dict[str, list[str]]:
    return {"families": sorted(model_registry.supported_model_ids())}


@router.post("")
def create_design(request: DesignCreateRequest) -> dict[str, object]:
    service = DesignService()
    result = service.generate(request.antenna_type, request.to_engineering_requirements())
    return success_response(result)


@router.post("/generate")
def generate_design(family: str, frequency_hz: float) -> dict[str, object]:
    service = DesignService()
    return service.generate(family, {"frequency_hz": frequency_hz})


@router.get("/{design_id}")
def get_design(design_id: str) -> dict[str, object]:
    return success_response(DesignService().get(design_id))


@router.patch("/{design_id}")
def update_design(design_id: str, request: DesignUpdateRequest) -> dict[str, object]:
    return success_response(DesignService().update(design_id, request.parameters))


@router.post("/{design_id}/validate")
def validate_design(design_id: str) -> dict[str, object]:
    design = DesignService().get(design_id)
    parameters = {**dict(design["parameters"]), "frequency_hz": design["frequency_hz"]}
    result = DesignService().validate_requirements(str(design["family"]), parameters)
    return success_response(result)


@router.post("/{design_id}/regenerate-geometry")
def regenerate_geometry(design_id: str) -> dict[str, object]:
    design = DesignService().get(design_id)
    return success_response(DesignService().update(design_id, dict(design["parameters"])))


@router.post("/{design_id}/revisions")
def create_revision(design_id: str) -> dict[str, object]:
    return success_response(DesignService().create_revision(design_id))
