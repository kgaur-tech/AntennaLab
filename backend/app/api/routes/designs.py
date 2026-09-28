from fastapi import APIRouter

from backend.app.core.errors import success_response
from backend.app.schemas.design_schema import DesignCreateRequest
from backend.app.services.design_service import DesignService
from backend.app.services.model_registry import model_registry

router = APIRouter(prefix="/designs", tags=["designs"])


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
