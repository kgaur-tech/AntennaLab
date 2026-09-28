"""Reusable structured validation utilities for engineering inputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from engineering.core.exceptions import InvalidEngineeringParameter


class ValidationStatus(str, Enum):
    MISSING = "missing"
    INVALID = "invalid"
    OUT_OF_RANGE = "out_of_range"
    UNSUPPORTED = "unsupported"
    VALID = "valid"


@dataclass
class ValidationIssue:
    field: str
    message: str
    status: ValidationStatus = ValidationStatus.INVALID
    severity: str = "error"


@dataclass
class ValidationResult:
    is_valid: bool
    issues: list[ValidationIssue] = field(default_factory=list)


def validate_positive_number(value: float, field_name: str) -> ValidationResult:
    result = ValidationResult(is_valid=True)
    if value is None:
        result.is_valid = False
        result.issues.append(ValidationIssue(field=field_name, message=f"{field_name} is required.", status=ValidationStatus.MISSING))
        return result
    if value <= 0:
        result.is_valid = False
        result.issues.append(ValidationIssue(field=field_name, message=f"{field_name} must be greater than zero.", status=ValidationStatus.INVALID))
    return result


def validate_frequency_range(f_min_hz: float, f_max_hz: float | None = None) -> ValidationResult:
    result = ValidationResult(is_valid=True)
    if f_min_hz <= 0:
        result.is_valid = False
        result.issues.append(ValidationIssue(field="frequency_hz", message="Frequency must be greater than zero.", status=ValidationStatus.INVALID))
    if f_max_hz is not None and f_max_hz < f_min_hz:
        result.is_valid = False
        result.issues.append(ValidationIssue(field="frequency_hz", message="Maximum frequency cannot be lower than minimum frequency.", status=ValidationStatus.INVALID))
    return result


def ensure_valid_parameters(params: dict[str, Any]) -> None:
    for key, value in params.items():
        if value is None:
            raise InvalidEngineeringParameter(f"Parameter '{key}' is required.")
        if isinstance(value, (int, float)) and value <= 0:
            raise InvalidEngineeringParameter(f"Parameter '{key}' must be positive.")


def validate_required_parameters(params: dict[str, Any], required: list[str]) -> ValidationResult:
    result = ValidationResult(is_valid=True)
    for name in required:
        if name not in params or params[name] is None:
            result.is_valid = False
            result.issues.append(ValidationIssue(field=name, message=f"{name} is required.", status=ValidationStatus.MISSING))
    return result
