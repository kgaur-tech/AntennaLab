"""Declarative capability registry for deterministic recommendation evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Directionality = Literal["omnidirectional", "directional"]


@dataclass(frozen=True)
class AntennaCapability:
    family: str
    model_version: str
    frequency_range_hz: tuple[float, float]
    polarizations: tuple[str, ...]
    directionality: Directionality
    size_factor_wavelengths: float
    simplicity: float
    supports_bandwidth_evaluation: bool
    supports_gain_evaluation: bool
    limitations: tuple[str, ...]


CAPABILITIES: dict[str, AntennaCapability] = {
    "dipole": AntennaCapability("dipole", "dipole-v1", (1e6, 1e12), ("linear", "horizontal", "vertical"), "omnidirectional", 0.5, 0.9, False, False, ("Installed-environment and feed effects are not modeled.",)),
    "monopole": AntennaCapability("monopole", "monopole-v1", (1e6, 1e12), ("linear", "vertical"), "omnidirectional", 0.25, 0.95, False, False, ("An electrically significant ground plane is assumed.",)),
    "yagi_uda": AntennaCapability("yagi_uda", "yagi-uda-v1", (1e6, 1e12), ("linear", "horizontal", "vertical"), "directional", 1.1, 0.35, False, False, ("Current Yagi-Uda model provides geometry only; gain and impedance are not calculated.",)),
}


def list_capabilities() -> tuple[AntennaCapability, ...]:
    return tuple(CAPABILITIES.values())
