"""Frequency conversion helpers for AntennaLab engineering calculations."""

from __future__ import annotations

from engineering.core.exceptions import InvalidEngineeringParameter


SUPPORTED_FREQUENCY_UNITS = {"hz", "khz", "mhz", "ghz"}


def _require_positive(value: float, label: str = "frequency") -> float:
    normalized = float(value)
    if normalized <= 0:
        raise InvalidEngineeringParameter(f"{label} must be greater than zero.")
    return normalized


def hz_to_mhz(value_hz: float) -> float:
    return float(value_hz) / 1_000_000.0


def hz_to_ghz(value_hz: float) -> float:
    return float(value_hz) / 1_000_000_000.0


def khz_to_hz(value_khz: float) -> float:
    return float(value_khz) * 1_000.0


def mhz_to_hz(value_mhz: float) -> float:
    return float(value_mhz) * 1_000_000.0


def ghz_to_hz(value_ghz: float) -> float:
    return float(value_ghz) * 1_000_000_000.0


def normalize_frequency(value: float, unit: str = "hz") -> float:
    """Normalize a positive frequency value to Hz."""
    frequency = _require_positive(value)
    normalized_unit = unit.lower()
    if normalized_unit == "hz":
        return frequency
    if normalized_unit == "khz":
        return khz_to_hz(frequency)
    if normalized_unit == "mhz":
        return mhz_to_hz(frequency)
    if normalized_unit == "ghz":
        return ghz_to_hz(frequency)
    raise InvalidEngineeringParameter(f"Unsupported frequency unit: {unit}.")
