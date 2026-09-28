"""Base interfaces and contracts for antenna model implementations."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import uuid5, NAMESPACE_URL

from engineering.core.geometry.model import GeometryModel


@dataclass
class DesignParameter:
    name: str
    value: float
    unit: str
    description: str = ""


@dataclass
class AntennaDesign:
    family: str
    model_version: str = "unversioned"
    design_id: str = ""
    frequency_hz: float = 0.0
    dimensions_m: dict[str, float] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    materials: dict[str, Any] = field(default_factory=dict)
    feed: dict[str, Any] = field(default_factory=dict)
    geometry: GeometryModel | None = None
    assumptions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def identity_payload(self, analysis_settings: dict[str, Any] | None = None) -> dict[str, Any]:
        return {
            "family": self.family,
            "model_version": self.model_version,
            "frequency_hz": self.frequency_hz,
            "parameters": self.parameters,
            "analysis_settings": analysis_settings or {},
        }

    def design_hash(self, analysis_settings: dict[str, Any] | None = None) -> str:
        payload = json.dumps(self.identity_payload(analysis_settings), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def ensure_design_id(self) -> None:
        if not self.design_id:
            self.design_id = str(uuid5(NAMESPACE_URL, self.design_hash()))

    def to_dict(self) -> dict[str, Any]:
        self.ensure_design_id()
        return {
            "design_id": self.design_id,
            "antenna_type": self.family,
            "family": self.family,
            "model_version": self.model_version,
            "frequency_hz": self.frequency_hz,
            "dimensions_m": self.dimensions_m,
            "parameters": self.parameters,
            "materials": self.materials,
            "feed": self.feed,
            "geometry": self.geometry.to_dict() if self.geometry else None,
            "assumptions": self.assumptions,
            "warnings": self.warnings,
            "design_hash": self.design_hash(),
        }


class AntennaModel(Protocol):
    family: str
    model_version: str

    def validate(self, parameters: dict[str, Any]) -> None:
        """Validate the model's required design parameters."""
        ...

    def calculate(self, parameters: dict[str, Any]) -> dict[str, Any]:
        """Calculate canonical design parameters from normalized inputs."""
        ...

    def generate_design(self, requirements: dict[str, Any]) -> AntennaDesign:
        """Generate a canonical design from requirement inputs."""
        ...

    def generate_geometry(self, design: AntennaDesign) -> GeometryModel:
        """Return engineering geometry for a generated design."""
        ...

    def evaluate(self, design: AntennaDesign) -> dict[str, Any]:
        """Return deterministic analytic metrics for a design."""
        ...

    def analyze(self, design: AntennaDesign, settings: dict[str, Any] | None = None) -> dict[str, Any]:
        """Analyze a generated design with supported deterministic methods."""
        ...

    def get_assumptions(self) -> list[str]:
        """Return assumption metadata for the model."""
        ...

    def get_validity_range(self) -> dict[str, tuple[float, float]]:
        """Return a structured validity envelope for model inputs."""
        ...

    def get_model_version(self) -> str:
        """Return the engineering model version."""
        ...
