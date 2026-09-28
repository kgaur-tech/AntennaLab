"""Monopole model using a quarter-wave approximation with explicit ground-plane assumptions."""

from __future__ import annotations

from typing import Any

from engineering.analysis.radiation import normalized_pattern_samples
from engineering.antennas.base import AntennaDesign
from engineering.analysis.result import AnalysisResult, ResultClass
from engineering.core.geometry.model import GeometryElement, GeometryModel
from engineering.core.math.wave import wavelength_m
from engineering.core.units.frequency import normalize_frequency
from engineering.core.validation.schema import ensure_valid_parameters


class MonopoleModel:
    family = "monopole"
    model_version = "monopole-v1"

    def validate(self, parameters: dict[str, Any]) -> None:
        ensure_valid_parameters(parameters)

    def calculate(self, parameters: dict[str, Any]) -> dict[str, Any]:
        frequency_hz = normalize_frequency(parameters["frequency_hz"], parameters.get("frequency_unit", "hz"))
        wavelength = wavelength_m(frequency_hz)
        total_length_m = wavelength / 4.0
        radius_m = parameters.get("radius_m", total_length_m / 100.0)
        self.validate({"frequency_hz": frequency_hz, "radius_m": radius_m})
        return {
            "frequency_hz": frequency_hz,
            "wavelength_m": wavelength,
            "total_length_m": total_length_m,
            "radius_m": radius_m,
        }

    def generate_design(self, requirements: dict[str, Any]) -> AntennaDesign:
        calculated = self.calculate(requirements)
        design = AntennaDesign(
            family=self.family,
            model_version=self.model_version,
            frequency_hz=calculated["frequency_hz"],
            dimensions_m={
                "total_length": calculated["total_length_m"],
                "radius": calculated["radius_m"],
            },
            parameters={
                "wavelength_m": calculated["wavelength_m"],
                "input_impedance_ohms": 36.5,
                "ground_plane_required": True,
                "length_factor": 0.25,
            },
            materials={"conductor": "wire"},
            feed={"impedance_ohms": 36.5, "type": "unbalanced"},
            assumptions=[
                "Quarter-wave monopole approximation.",
                "Ground plane is assumed to be present and electrically significant.",
            ],
            warnings=["This model does not include complex feed or platform coupling effects."],
        )
        design.geometry = self.generate_geometry(design)
        design.ensure_design_id()
        return design

    def generate_geometry(self, design: AntennaDesign) -> GeometryModel:
        total_length = design.dimensions_m["total_length"]
        geometry = GeometryModel(
            family=self.family,
            metadata={"source": "analytical", "model": self.model_version},
        )
        geometry.add_element(
            GeometryElement(
                name="monopole",
                kind="wire",
                length_m=total_length,
                radius_m=design.dimensions_m["radius"],
                position_m=(0.0, 0.0, 0.0),
                orientation_deg=90.0,
                metadata={"axis": "z"},
            )
        )
        return geometry

    def analyze(self, design: AntennaDesign, settings: dict[str, Any] | None = None) -> dict[str, Any]:
        settings = settings or {}
        sample_count = int(settings.get("sample_count", 91))
        result = AnalysisResult(
            model_type=self.family,
            model_version=self.model_version,
            result_class=ResultClass.CALCULATED,
            inputs={"frequency_hz": design.frequency_hz},
            metrics={
                "wavelength_m": design.parameters["wavelength_m"],
                "electrical_length_wavelengths": 0.25,
                "theoretical_directivity_dbi_over_ideal_ground": 5.15,
                "reference_input_impedance_ohms": 36.5,
            },
            geometry_reference={"design_id": design.design_id, "design_hash": design.design_hash(settings)},
            plots=[
                {
                    "name": "upper_hemisphere_normalized_power",
                    "result_class": ResultClass.CALCULATED.value,
                    "data": normalized_pattern_samples("monopole_upper_hemisphere", sample_count),
                }
            ],
            assumptions=design.assumptions,
            warnings=design.warnings,
            validity="valid",
            computation_metadata={
                "method": "quarter-wave monopole image-theory approximation over ideal ground",
                "references": ["Balanis antenna theory: monopole over perfectly conducting ground plane"],
            },
        )
        return result.to_dict()

    def evaluate(self, design: AntennaDesign) -> dict[str, Any]:
        return self.analyze(design)

    def get_assumptions(self) -> list[str]:
        return [
            "Quarter-wave monopole approximation.",
            "Ground plane is assumed to be present and electrically significant.",
        ]

    def get_validity_range(self) -> dict[str, tuple[float, float]]:
        return {"frequency_hz": (1e6, 1e12)}

    def get_model_version(self) -> str:
        return self.model_version


Monopole = MonopoleModel

__all__ = ["MonopoleModel", "Monopole"]
