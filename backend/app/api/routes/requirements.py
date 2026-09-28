from fastapi import APIRouter

from backend.app.core.errors import success_response
from backend.app.models.requirement import AntennaRequirement
from backend.app.schemas.design_schema import RequirementValidationRequest
from backend.app.schemas.requirement_schema import RequirementSchema
from backend.app.services.design_service import DesignService
from backend.app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/requirements", tags=["requirements"])


@router.post("/recommend")
def recommend_antennas(requirement: RequirementSchema) -> dict[str, object]:
    service = RecommendationService()
    payload = requirement.model_dump()
    payload["frequency_hz"] = requirement.normalized_frequency_hz()
    payload.pop("frequency", None)
    payload.pop("frequency_unit", None)
    recommendations = service.recommend(AntennaRequirement(**payload))
    return success_response({"recommendations": [candidate.__dict__ for candidate in recommendations]})


@router.post("/validate")
def validate_requirements(request: RequirementValidationRequest) -> dict[str, object]:
    service = DesignService()
    result = service.validate_requirements(request.antenna_type, request.to_engineering_requirements())
    return success_response(result)
