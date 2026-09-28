from fastapi import APIRouter

from backend.app.api.routes.designs import router as designs_router
from backend.app.api.routes.models import router as models_router
from backend.app.api.routes.requirements import router as requirements_router

api_router = APIRouter()
api_router.include_router(requirements_router)
api_router.include_router(designs_router)
api_router.include_router(models_router)
