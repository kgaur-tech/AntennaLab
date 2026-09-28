"""Angle conversion helpers for AntennaLab engineering calculations."""

from __future__ import annotations

import math


def deg_to_rad(value_deg: float) -> float:
    return math.radians(float(value_deg))


def rad_to_deg(value_rad: float) -> float:
    return math.degrees(float(value_rad))
