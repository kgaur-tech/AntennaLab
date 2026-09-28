"""Reusable project-wide result schema for antenna computation outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ResultClass(str, Enum):
    CALCULATED = "CALCULATED"
    PREDICTED = "PREDICTED"
    SIMULATED = "SIMULATED"
    MEASURED = "MEASURED"


@dataclass
class AnalysisResult:
    model_type: str
    model_version: str
    result_class: ResultClass | str
    inputs: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, Any] = field(default_factory=dict)
    geometry_reference: dict[str, Any] | None = None
    plots: list[dict[str, Any]] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    validity: str = "valid"
    computation_metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_type": self.model_type,
            "model_version": self.model_version,
            "result_class": self.result_class.value if isinstance(self.result_class, ResultClass) else self.result_class,
            "inputs": self.inputs,
            "metrics": self.metrics,
            "geometry_reference": self.geometry_reference,
            "plots": self.plots,
            "assumptions": self.assumptions,
            "warnings": self.warnings,
            "validity": self.validity,
            "computation_metadata": self.computation_metadata,
        }
