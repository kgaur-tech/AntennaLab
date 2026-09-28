"""Length conversion helpers for AntennaLab engineering calculations."""

from __future__ import annotations

from engineering.core.exceptions import InvalidEngineeringParameter


SUPPORTED_LENGTH_UNITS = {"m", "cm", "mm"}


def _require_positive(value: float, label: str = "length") -> float:
    normalized = float(value)
    if normalized <= 0:
        raise InvalidEngineeringParameter(f"{label} must be greater than zero.")
    return normalized


def mm_to_m(value_mm: float) -> float:
    return float(value_mm) / 1000.0


def cm_to_m(value_cm: float) -> float:
    return float(value_cm) / 100.0


def m_to_mm(value_m: float) -> float:
    return float(value_m) * 1000.0


def m_to_cm(value_m: float) -> float:
    return float(value_m) * 100.0


def normalize_length(value: float, unit: str = "m") -> float:
    """Normalize a positive length value to meters."""
    length = _require_positive(value)
    normalized_unit = unit.lower()
    if normalized_unit == "m":
        return length
    if normalized_unit == "cm":
        return cm_to_m(length)
    if normalized_unit == "mm":
        return mm_to_m(length)
    raise InvalidEngineeringParameter(f"Unsupported length unit: {unit}.")
