"""Analytical radiation and pattern helpers."""

from __future__ import annotations

import math


def free_space_wavelength_hz(frequency_hz: float) -> float:
    if frequency_hz <= 0:
        raise ValueError("Frequency must be positive.")
    return 299_792_458.0 / frequency_hz


def effective_aperture(m2: float, gain_linear: float) -> float:
    if m2 <= 0:
        raise ValueError("Aperture area must be positive.")
    return m2 * gain_linear


def db_to_linear(db_value: float) -> float:
    return 10.0 ** (db_value / 10.0)


def linear_to_db(linear_value: float) -> float:
    if linear_value <= 0:
        raise ValueError("Linear power ratio must be positive.")
    return 10.0 * math.log10(linear_value)
