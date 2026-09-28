"""Dipole model with deterministic analytical calculations and canonical geometry."""

from __future__ import annotations

from typing import Any

from engineering.analysis.radiation import normalized_pattern_samples
from engineering.antennas.base import AntennaDesign
from engineering.analysis.result import AnalysisResult, ResultClass
from engineering.core.geometry.model import GeometryElement, GeometryModel
from engineering.core.math.wave import wavelength_m
from engineering.core.units.frequency import normalize_frequency
from engineering.core.validation.schema import ensure_valid_parameters


class DipoleModel:
    family = "dipole"
    model_version = "dipole-v1"

    def validate(self, parameters: dict[str, Any]) -> None:
        ensure_valid_parameters(parameters)

    def calculate(self, parameters: dict[str, Any]) -> dict[str, Any]:
        frequency_hz = normalize_frequency(parameters["frequency_hz"], parameters.get("frequency_unit", "hz"))
        radius_m = parameters.get("radius_m", wavelength_m(frequency_hz) / 400.0)
        self.validate({"frequency_hz": frequency_hz, "radius_m": radius_m})
        wavelength = wavelength_m(frequency_hz)
        total_length_m = wavelength / 2.0
        return {
            "frequency_hz": frequency_hz,
            "wavelength_m": wavelength,
            "total_length_m": total_length_m,
            "half_length_m": total_length_m / 2.0,
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
                "half_length": calculated["half_length_m"],
                "radius": calculated["radius_m"],
            },
            parameters={
                "wavelength_m": calculated["wavelength_m"],
                "feed_impedance_ohms": 73.0,
                "element_count": 2,
                "length_factor": 0.5,
            },
            materials={"conductor": "wire"},
            feed={"impedance_ohms": 73.0, "type": "balanced"},
            assumptions=[
                "Half-wave dipole approximation.",
                "Free-space environment for initial estimate.",
            ],
            warnings=[],
        )
        design.geometry = self.generate_geometry(design)
        design.ensure_design_id()
        return design

    def generate_geometry(self, design: AntennaDesign) -> GeometryModel:
        total_length = design.dimensions_m["total_length"]
        half_length = total_length / 2.0
        geometry = GeometryModel(
            family=self.family,
            metadata={"source": "analytical", "model": self.model_version},
        )
        geometry.add_element(
            GeometryElement(
                name="left_arm",
                kind="wire",
                length_m=half_length,
                radius_m=design.dimensions_m["radius"],
                position_m=(-half_length / 2.0, 0.0, 0.0),
                orientation_deg=0.0,
                metadata={"axis": "x"},
            )
        )
        geometry.add_element(
            GeometryElement(
                name="right_arm",
                kind="wire",
                length_m=half_length,
                radius_m=design.dimensions_m["radius"],
                position_m=(half_length / 2.0, 0.0, 0.0),
                orientation_deg=0.0,
                metadata={"axis": "x"},
            )
        )
        return geometry

    def analyze(self, design: AntennaDesign, settings: dict[str, Any] | None = None) -> dict[str, Any]:
        settings = settings or {}
        sample_count = int(settings.get("sample_count", 181))
        result = AnalysisResult(
            model_type=self.family,
            model_version=self.model_version,
            result_class=ResultClass.CALCULATED,
            inputs={"frequency_hz": design.frequency_hz},
            metrics={
                "wavelength_m": design.parameters["wavelength_m"],
                "electrical_length_wavelengths": 0.5,
                "theoretical_directivity_dbi": 2.15,
                "reference_input_impedance_ohms": 73.0,
            },
            geometry_reference={"design_id": design.design_id, "design_hash": design.design_hash(settings)},
            plots=[
                {
                    "name": "e_plane_normalized_power",
                    "result_class": ResultClass.CALCULATED.value,
                    "data": normalized_pattern_samples("half_wave_dipole_e_plane", sample_count),
                }
            ],
            assumptions=design.assumptions,
            warnings=design.warnings,
            validity="valid",
            computation_metadata={
                "method": "thin half-wave dipole closed-form approximation",
                "references": ["Balanis antenna theory: center-fed thin half-wave dipole reference behavior"],
            },
        )
        return result.to_dict()

    def evaluate(self, design: AntennaDesign) -> dict[str, Any]:
        return self.analyze(design)

    def get_assumptions(self) -> list[str]:
        return [
            "Half-wave dipole approximation.",
            "Free-space environment for initial estimate.",
        ]

    def get_validity_range(self) -> dict[str, tuple[float, float]]:
        return {"frequency_hz": (1e6, 1e12)}

    def get_model_version(self) -> str:
        return self.model_version


Dipole = DipoleModel

__all__ = ["DipoleModel", "Dipole"]
