"""Canonical geometry representation used by the engineering layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GeometryElement:
    name: str
    kind: str
    length_m: float | None = None
    radius_m: float | None = None
    position_m: tuple[float, float, float] = (0.0, 0.0, 0.0)
    orientation_deg: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "kind": self.kind,
            "length_m": self.length_m,
            "radius_m": self.radius_m,
            "position_m": self.position_m,
            "orientation_deg": self.orientation_deg,
            "metadata": self.metadata,
        }


@dataclass
class GeometryModel:
    family: str
    elements: list[GeometryElement] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_element(self, element: GeometryElement) -> None:
        self.elements.append(element)

    def to_dict(self) -> dict[str, Any]:
        return {
            "family": self.family,
            "elements": [element.to_dict() for element in self.elements],
            "metadata": self.metadata,
        }
