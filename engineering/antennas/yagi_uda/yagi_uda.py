"""Yagi-Uda model with parameterized geometry and explicit canonical element control."""

from __future__ import annotations

from typing import Any

from engineering.antennas.base import AntennaDesign
from engineering.analysis.result import AnalysisResult, ResultClass
from engineering.core.geometry.model import GeometryElement, GeometryModel
from engineering.core.math.wave import wavelength_m
from engineering.core.units.frequency import normalize_frequency
from engineering.core.validation.schema import ensure_valid_parameters


class YagiUdaModel:
    family = "yagi_uda"
    model_version = "yagi-uda-v1"

    def validate(self, parameters: dict[str, Any]) -> None:
        ensure_valid_parameters(parameters)
        if "director_count" in parameters and parameters["director_count"] < 1:
            raise ValueError("director_count must be at least 1.")
        if "director_lengths" in parameters and len(parameters["director_lengths"]) != int(parameters["director_count"]):
            raise ValueError("director_lengths must match director_count.")
        if "director_lengths" in parameters and any(length <= 0 for length in parameters["director_lengths"]):
            raise ValueError("director_lengths values must be positive.")
        if "element_spacings" in parameters and len(parameters["element_spacings"]) != int(parameters["director_count"]) + 1:
            raise ValueError("element_spacings must include reflector-to-driven plus driven/director intervals.")
        if "element_spacings" in parameters and any(spacing <= 0 for spacing in parameters["element_spacings"]):
            raise ValueError("element_spacings values must be positive.")

    def calculate(self, parameters: dict[str, Any]) -> dict[str, Any]:
        frequency_hz = normalize_frequency(parameters["frequency_hz"], parameters.get("frequency_unit", "hz"))
        director_count = int(parameters.get("director_count", parameters.get("number_of_directors", 3)))
        self.validate({"frequency_hz": frequency_hz, "director_count": director_count})
        wavelength = wavelength_m(frequency_hz)
        reflector_length_m = float(parameters.get("reflector_length_m", wavelength * 0.52))
        driven_length_m = float(parameters.get("driven_element_length_m", wavelength * 0.47))
        director_lengths = parameters.get("director_lengths_m")
        if director_lengths is None:
            director_lengths = [wavelength * (0.45 - 0.005 * index) for index in range(director_count)]
        director_lengths = [float(length) for length in director_lengths]
        element_spacings = parameters.get("element_spacings_m")
        if element_spacings is None:
            element_spacings = [wavelength * 0.20] + [wavelength * 0.15 for _ in range(director_count)]
        element_spacings = [float(spacing) for spacing in element_spacings]
        self.validate({
            "frequency_hz": frequency_hz,
            "director_count": director_count,
            "reflector_length": reflector_length_m,
            "driven_length": driven_length_m,
            "director_lengths": director_lengths,
            "element_spacings": element_spacings,
            "element_radius": float(parameters.get("element_radius_m", wavelength / 400.0)),
        })
        return {
            "frequency_hz": frequency_hz,
            "wavelength_m": wavelength,
            "director_count": director_count,
            "reflector_length_m": reflector_length_m,
            "driven_element_length_m": driven_length_m,
            "director_lengths_m": director_lengths,
            "element_spacings_m": element_spacings,
            "boom_length_m": sum(element_spacings),
            "element_radius_m": float(parameters.get("element_radius_m", wavelength / 400.0)),
        }

    def generate_design(self, requirements: dict[str, Any]) -> AntennaDesign:
        calculated = self.calculate(requirements)
        director_lengths = calculated["director_lengths_m"]
        element_spacings = calculated["element_spacings_m"]

        design = AntennaDesign(
            family=self.family,
            model_version=self.model_version,
            frequency_hz=calculated["frequency_hz"],
            dimensions_m={
                "reflector_length": calculated["reflector_length_m"],
                "driven_element_length": calculated["driven_element_length_m"],
                "director_lengths": director_lengths,
                "element_spacings": element_spacings,
                "boom_length": calculated["boom_length_m"],
                "element_radius": calculated["element_radius_m"],
                **{f"director_{index}_length": length for index, length in enumerate(director_lengths, start=1)},
            },
            parameters={
                "wavelength_m": calculated["wavelength_m"],
                "director_count": calculated["director_count"],
                "number_of_directors": calculated["director_count"],
                "reflector_length_m": calculated["reflector_length_m"],
                "driven_element_length_m": calculated["driven_element_length_m"],
                "director_lengths": director_lengths,
                "director_lengths_m": director_lengths,
                "element_spacings_m": element_spacings,
                "boom_length_m": calculated["boom_length_m"],
                "element_radius_m": calculated["element_radius_m"],
            },
            materials={"boom": "metal", "elements": "wire"},
            feed={"impedance_ohms": 50.0, "type": "balanced"},
            assumptions=[
                "Simplified canonical Yagi-Uda dimensional heuristic.",
                "Directional gain estimate is based on an analytical approximation.",
            ],
            warnings=["This model is heuristic and should be followed by higher-fidelity validation for production designs."],
        )
        design.geometry = self.generate_geometry(design)
        design.ensure_design_id()
        return design

    def generate_geometry(self, design: AntennaDesign) -> GeometryModel:
        element_spacings = design.parameters["element_spacings_m"]
        geometry = GeometryModel(
            family=self.family,
            metadata={"source": "heuristic", "model": self.model_version},
        )
        reflector_length = design.parameters["reflector_length_m"]
        driven_length = design.parameters["driven_element_length_m"]
        director_lengths = design.parameters["director_lengths_m"]
        element_radius = design.parameters["element_radius_m"]

        reflector_x = -element_spacings[0]
        geometry.add_element(GeometryElement("reflector", "wire", length_m=reflector_length, radius_m=element_radius, position_m=(reflector_x, 0.0, 0.0), orientation_deg=90.0, metadata={"role": "reflector", "axis": "y"}))
        geometry.add_element(GeometryElement("driven_element", "wire", length_m=driven_length, radius_m=element_radius, position_m=(0.0, 0.0, 0.0), orientation_deg=90.0, metadata={"role": "driven", "axis": "y"}))

        current_x = 0.0
        for index, director_length in enumerate(director_lengths, start=1):
            current_x += element_spacings[index]
            geometry.add_element(
                GeometryElement(
                    f"director_{index}",
                    "wire",
                    length_m=director_length,
                    radius_m=element_radius,
                    position_m=(current_x, 0.0, 0.0),
                    orientation_deg=90.0,
                    metadata={"role": "director", "index": index, "axis": "y", "parameter": f"director_{index}_length"},
                )
            )
        return geometry

    def analyze(self, design: AntennaDesign, settings: dict[str, Any] | None = None) -> dict[str, Any]:
        settings = settings or {}
        result = AnalysisResult(
            model_type=self.family,
            model_version=self.model_version,
            result_class=ResultClass.CALCULATED,
            inputs={"frequency_hz": design.frequency_hz},
            metrics={
                "wavelength_m": design.parameters["wavelength_m"],
                "element_count": len(design.geometry.elements) if design.geometry else 0,
                "director_count": len(design.parameters.get("director_lengths", [])),
                "boom_length_m": design.parameters["boom_length_m"],
            },
            geometry_reference={"design_id": design.design_id, "design_hash": design.design_hash(settings)},
            assumptions=design.assumptions,
            warnings=design.warnings + ["Yagi-Uda radiation, impedance, gain, and front-to-back ratio are not calculated by this Phase 1 model."],
            validity="heuristic",
            computation_metadata={
                "method": "canonical dimensional heuristic only",
                "references": ["Common introductory Yagi-Uda proportional design rules; production validation requires higher-fidelity analysis."],
            },
        )
        return result.to_dict()

    def evaluate(self, design: AntennaDesign) -> dict[str, Any]:
        return self.analyze(design)

    def get_assumptions(self) -> list[str]:
        return [
            "Simplified canonical Yagi-Uda dimensional heuristic.",
            "Directional gain estimate is based on an analytical approximation.",
            "Director lengths are parameterized individually for later optimization.",
        ]

    def get_validity_range(self) -> dict[str, tuple[float, float]]:
        return {"frequency_hz": (1e6, 1e12), "director_count": (1.0, 20.0)}

    def get_model_version(self) -> str:
        return self.model_version


YagiUda = YagiUdaModel

__all__ = ["YagiUdaModel", "YagiUda"]
