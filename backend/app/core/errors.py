from __future__ import annotations

import logging
from dataclasses import dataclass, field as dataclass_field
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from engineering.core.exceptions import (
    EngineeringError,
    InvalidEngineeringParameter,
    InvalidGeometry,
    ModelOutsideValidityRange,
    UnsupportedAnalysis,
    UnsupportedFrequencyRange,
)

logger = logging.getLogger(__name__)


@dataclass
class ApiError:
    code: str
    message: str
    field: str | None = None
    details: dict[str, Any] = dataclass_field(default_factory=dict)

    def to_response(self) -> dict[str, Any]:
        return {
            "success": False,
            "error": {
                "code": self.code,
                "message": self.message,
                "field": self.field,
                "details": self.details,
            },
        }


class ApiException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        field: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.error = ApiError(code=code, message=message, field=field, details=details or {})
        self.status_code = status_code
        super().__init__(message)


class UnsupportedModelException(ApiException):
    def __init__(self, antenna_type: str) -> None:
        super().__init__(
            code="UNSUPPORTED_ANTENNA_TYPE",
            message=f"Unsupported antenna type: {antenna_type}.",
            status_code=400,
            field="antenna_type",
            details={"antenna_type": antenna_type},
        )


def success_response(data: Any) -> dict[str, Any]:
    return {"success": True, "data": data}


def map_engineering_error(exc: EngineeringError) -> ApiException:
    message = str(exc)
    if isinstance(exc, UnsupportedFrequencyRange):
        return ApiException("UNSUPPORTED_FREQUENCY_RANGE", message, 400, "frequency")
    if isinstance(exc, ModelOutsideValidityRange):
        return ApiException("MODEL_OUTSIDE_VALIDITY_RANGE", message, 400)
    if isinstance(exc, InvalidGeometry):
        return ApiException("INVALID_GEOMETRY", message, 400)
    if isinstance(exc, UnsupportedAnalysis):
        return ApiException("UNSUPPORTED_ANALYSIS", message, 400)
    if isinstance(exc, InvalidEngineeringParameter):
        return ApiException("INVALID_ENGINEERING_PARAMETER", message, 400)
    return ApiException("ENGINEERING_ERROR", message, 400)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiException)
    async def api_exception_handler(_: Request, exc: ApiException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content=exc.error.to_response())

    @app.exception_handler(EngineeringError)
    async def engineering_exception_handler(_: Request, exc: EngineeringError) -> JSONResponse:
        api_error = map_engineering_error(exc)
        return JSONResponse(status_code=api_error.status_code, content=api_error.error.to_response())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        first_error = exc.errors()[0] if exc.errors() else {}
        location = first_error.get("loc", [])
        field = str(location[-1]) if location else None
        message = first_error.get("msg", "Request validation failed.")
        error = ApiError(
            code="VALIDATION_ERROR",
            message=message,
            field=field,
            details={"errors": exc.errors()},
        )
        return JSONResponse(status_code=422, content=error.to_response())

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unexpected backend error", exc_info=exc)
        error = ApiError(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected server error occurred.",
        )
        return JSONResponse(status_code=500, content=error.to_response())
