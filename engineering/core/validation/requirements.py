"""Requirement validation helpers for antenna specification intake."""

from __future__ import annotations


def validate_frequency_range(f_min_hz: float, f_max_hz: float) -> None:
    if f_min_hz <= 0 or f_max_hz <= 0:
        raise ValueError("Frequency values must be positive.")
    if f_max_hz < f_min_hz:
        raise ValueError("Maximum frequency must be greater than or equal to minimum frequency.")


def validate_length(value_m: float, label: str = "dimension") -> None:
    if value_m <= 0:
        raise ValueError(f"{label} must be greater than zero.")


def validate_gain_db(value_db: float) -> None:
    if value_db < -100 or value_db > 100:
        raise ValueError("Gain value is out of a realistic engineering range.")
