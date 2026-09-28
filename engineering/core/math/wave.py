"""Wave-related analytical helpers for antenna calculations."""

from __future__ import annotations

from engineering.core.constants.physics import C0
from engineering.core.exceptions import InvalidEngineeringParameter


def wavelength_m(frequency_hz: float) -> float:
    if frequency_hz <= 0:
        raise InvalidEngineeringParameter("Frequency must be positive.")
    return C0 / frequency_hz


def electrical_length_m(length_m: float, frequency_hz: float) -> float:
    if length_m <= 0:
        raise InvalidEngineeringParameter("Length must be positive.")
    return length_m / wavelength_m(frequency_hz)
