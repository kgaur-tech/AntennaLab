from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class AntennaRequirement:
    application: str
    frequency_hz: float
    bandwidth_hz: float | None = None
    gain_db: float | None = None
    polarization: str = "linear"
    is_directional: bool = True
    max_dimension_m: float | None = None
    target_impedance_ohms: float = 50.0
    environment: str = "general"
    notes: str = ""
    priority_weights: dict[str, float] = field(default_factory=lambda: {
        "gain": 1.0,
        "size": 1.0,
        "bandwidth": 1.0,
    })
    antenna_family_preferences: list[str] = field(default_factory=list)


@dataclass
class RecommendationCandidate:
    family: str
    score: float
    reasons: list[str] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)
