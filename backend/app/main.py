from fastapi import FastAPI

from backend.app.api.router import api_router
from backend.app.core.config import get_settings
from backend.app.core.errors import register_error_handlers

def create_app() -> FastAPI:
    """Create the HTTP application without coupling startup to module import."""
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="AntennaLab deterministic RF engineering API.",
        debug=settings.debug,
    )
    register_error_handlers(application)
    application.include_router(api_router, prefix=settings.api_prefix)

    @application.get("/health", tags=["operations"])
    def healthcheck() -> dict[str, str]:
        return {"status": "ok", "service": settings.app_name, "environment": settings.environment}

    return application


app = create_app()
