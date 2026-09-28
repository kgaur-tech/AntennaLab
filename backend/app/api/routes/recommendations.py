from fastapi import APIRouter

from backend.app.core.errors import success_response
from backend.app.models.requirement import AntennaRequirement
from backend.app.schemas.requirement_schema import RequirementSchema
from backend.app.services.explainable_recommendation_service import ExplainableRecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("")
def generate_recommendations(requirement: RequirementSchema) -> dict[str, object]:
    payload = requirement.model_dump()
    payload["frequency_hz"] = requirement.normalized_frequency_hz()
    payload.pop("frequency", None)
    payload.pop("frequency_unit", None)
    return success_response(ExplainableRecommendationService().recommend(AntennaRequirement(**payload)))
