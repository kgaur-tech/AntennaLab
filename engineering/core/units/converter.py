"""Unit conversion helpers for RF engineering calculations."""

from __future__ import annotations

from engineering.core.units.frequency import normalize_frequency
from engineering.core.units.length import normalize_length


def to_meters(length_m: float) -> float:
    """Return the length value in meters assuming the input is already in meters."""
    return float(length_m)


def mhz_to_hz(freq_mhz: float) -> float:
    return float(freq_mhz) * 1_000_000.0


def ghz_to_hz(freq_ghz: float) -> float:
    return float(freq_ghz) * 1_000_000_000.0


def mm_to_m(length_mm: float) -> float:
    return float(length_mm) / 1000.0


def cm_to_m(length_cm: float) -> float:
    return float(length_cm) / 100.0


def normalize_value(value: float, unit: str, quantity: str) -> float:
    """Normalize a scalar engineering value into the internal SI base unit."""
    if quantity == "frequency":
        return normalize_frequency(value, unit)
    if quantity == "length":
        return normalize_length(value, unit)
    raise ValueError(f"Unsupported quantity for normalization: {quantity}.")
