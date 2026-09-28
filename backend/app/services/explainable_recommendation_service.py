"""Versioned deterministic recommendation engine with inspectable decisions."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Literal

from engineering.core.math.wave import wavelength_m

from backend.app.models.requirement import AntennaRequirement
from backend.app.services.antenna_capabilities import AntennaCapability, list_capabilities

ENGINE_VERSION = "recommendation-engine-v1"


@dataclass(frozen=True)
class ScoreComponent:
    criterion: str
    status: Literal["EVALUATED", "NOT_EVALUATED", "UNSUPPORTED"]
    score: float | None
    reason_code: str
    message: str


@dataclass
class CandidateEvaluation:
    family: str
    model_version: str
    status: Literal["eligible", "excluded"]
    score: float | None
    hard_constraints: list[ScoreComponent] = field(default_factory=list)
    score_components: list[ScoreComponent] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    tradeoffs: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        return result


class ExplainableRecommendationService:
    """Hard constraints exclude candidates before deterministic soft scoring."""

    def recommend(self, requirement: AntennaRequirement) -> dict[str, object]:
        candidates = [self._evaluate(requirement, capability) for capability in list_capabilities()]
        eligible = sorted((item for item in candidates if item.status == "eligible"), key=lambda item: (-float(item.score or 0), item.family))
        excluded = sorted((item for item in candidates if item.status == "excluded"), key=lambda item: item.family)
        return {
            "engine_version": ENGINE_VERSION,
            "requirement": asdict(requirement),
            "recommended": [eligible[0].to_dict()] if eligible else [],
            "alternatives": [item.to_dict() for item in eligible[1:]],
            "excluded_candidates": [item.to_dict() for item in excluded],
            "warnings": self._requirement_warnings(requirement),
        }

    def _evaluate(self, requirement: AntennaRequirement, capability: AntennaCapability) -> CandidateEvaluation:
        hard = self._hard_constraints(requirement, capability)
        failure_codes = {"FREQUENCY_UNSUPPORTED", "DIRECTIONALITY_MISMATCH", "POLARIZATION_UNSUPPORTED", "SIZE_LIMIT_EXCEEDED"}
        failures = [item for item in hard if item.reason_code in failure_codes]
        if failures:
            return CandidateEvaluation(capability.family, capability.model_version, "excluded", None, hard_constraints=hard, reasons=[item.message for item in failures], warnings=list(capability.limitations))
        components = self._soft_components(requirement, capability)
        evaluated = [item for item in components if item.status == "EVALUATED" and item.score is not None]
        weights = requirement.priority_weights
        total_weight = sum(float(weights.get(item.criterion, 1.0)) for item in evaluated)
        score = 100 * sum(float(item.score) * float(weights.get(item.criterion, 1.0)) for item in evaluated) / total_weight if total_weight else 0.0
        return CandidateEvaluation(capability.family, capability.model_version, "eligible", round(score, 2), hard_constraints=hard, score_components=components, reasons=[item.message for item in hard if item.reason_code.endswith("MATCH")], tradeoffs=[item.message for item in evaluated if item.score is not None and item.score < 0.75], warnings=list(capability.limitations) + [item.message for item in components if item.status != "EVALUATED"])

    def _hard_constraints(self, requirement: AntennaRequirement, capability: AntennaCapability) -> list[ScoreComponent]:
        items: list[ScoreComponent] = []
        frequency_ok = capability.frequency_range_hz[0] <= requirement.frequency_hz <= capability.frequency_range_hz[1]
        items.append(ScoreComponent("frequency", "EVALUATED", float(frequency_ok), "FREQUENCY_SUPPORTED" if frequency_ok else "FREQUENCY_UNSUPPORTED", "Frequency is within the model validity range." if frequency_ok else "Frequency is outside the model validity range."))
        directionality = getattr(requirement, "directionality", "no_preference")
        if directionality != "no_preference":
            required = "directional" if directionality in {"directional", "highly_directional"} else "omnidirectional"
            matched = required == capability.directionality
            items.append(ScoreComponent("directionality", "EVALUATED", float(matched), "DIRECTIONALITY_MATCH" if matched else "DIRECTIONALITY_MISMATCH", "Directionality requirement is supported." if matched else "Directionality requirement is not supported by this model."))
        if requirement.polarization not in {"no_preference", "custom"}:
            matched = requirement.polarization in capability.polarizations
            items.append(ScoreComponent("polarization", "EVALUATED", float(matched), "POLARIZATION_MATCH" if matched else "POLARIZATION_UNSUPPORTED", "Polarization requirement is supported." if matched else "Polarization requirement is not supported by this model."))
        if requirement.max_dimension_m is not None:
            matched = wavelength_m(requirement.frequency_hz) * capability.size_factor_wavelengths <= requirement.max_dimension_m
            items.append(ScoreComponent("size", "EVALUATED", float(matched), "SIZE_CONSTRAINT_MATCH" if matched else "SIZE_LIMIT_EXCEEDED", "Canonical dimensional envelope fits the stated maximum." if matched else "Canonical dimensional envelope exceeds the stated maximum."))
        return items

    def _soft_components(self, requirement: AntennaRequirement, capability: AntennaCapability) -> list[ScoreComponent]:
        items = [ScoreComponent("simplicity", "EVALUATED", capability.simplicity, "SIMPLICITY_FIT", "Fabrication simplicity was evaluated from registered model characteristics.")]
        if requirement.max_dimension_m is None:
            items.append(ScoreComponent("size", "NOT_EVALUATED", None, "SIZE_NOT_SPECIFIED", "No maximum dimension was supplied."))
        else:
            fit = min(1.0, requirement.max_dimension_m / (wavelength_m(requirement.frequency_hz) * capability.size_factor_wavelengths))
            items.append(ScoreComponent("size", "EVALUATED", fit, "SIZE_FIT", "Size preference was evaluated after the hard check."))
        items.extend([ScoreComponent("gain", "UNSUPPORTED", None, "GAIN_NOT_EVALUATED", "Current model does not evaluate gain compatibility."), ScoreComponent("bandwidth", "UNSUPPORTED", None, "BANDWIDTH_NOT_EVALUATED", "Current model does not evaluate bandwidth compatibility.")])
        return items

    @staticmethod
    def _requirement_warnings(requirement: AntennaRequirement) -> list[str]:
        if requirement.environment not in {"general", "free_space"}:
            return ["Current models do not calculate mounting or platform coupling effects for the selected environment."]
        return []
