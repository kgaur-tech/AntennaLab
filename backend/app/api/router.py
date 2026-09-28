from fastapi import APIRouter

from backend.app.api.routes.designs import router as designs_router
from backend.app.api.routes.models import router as models_router
from backend.app.api.routes.requirements import router as requirements_router
from backend.app.api.routes.recommendations import router as recommendations_router
from backend.app.api.routes.analysis import router as analysis_router
from backend.app.api.routes.sweeps import router as sweeps_router

api_router = APIRouter()
api_router.include_router(requirements_router)
api_router.include_router(designs_router)
api_router.include_router(models_router)
api_router.include_router(recommendations_router)
api_router.include_router(analysis_router)
api_router.include_router(sweeps_router)
