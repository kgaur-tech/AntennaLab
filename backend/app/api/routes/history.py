from fastapi import APIRouter

from backend.app.core.errors import success_response
from backend.app.services.history_service import history_service

router = APIRouter(tags=["history"])

@router.get("/designs/{design_id}/revisions")
def list_revisions(design_id: str) -> dict[str, object]: return success_response({"revisions": history_service.list_revisions(design_id)})

@router.get("/designs/{design_id}/compare")
def compare_revisions(design_id: str, left: int, right: int) -> dict[str, object]: return success_response(history_service.compare(design_id, left, right))

@router.get("/designs/{design_id}/datasheet")
def datasheet(design_id: str, revision: int | None = None) -> dict[str, object]: return success_response(history_service.datasheet(design_id, revision))
