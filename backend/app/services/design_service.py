from __future__ import annotations

from typing import Any

from engineering.core.exceptions import EngineeringError

from backend.app.core.errors import ApiException, map_engineering_error
from backend.app.models.design import DesignRecord, DesignRevisionRecord
from backend.app.services.model_registry import model_registry


class DesignService:
    """Coordinates deterministic design generation for the supported antenna families."""

    def __init__(self) -> None:
        self.registry = model_registry

    def generate(self, family: str, requirements: dict[str, Any]) -> dict[str, Any]:
        try:
            model = self.registry.create(family)
            registration = self.registry.get_registration(family)
            design = model.generate_design(requirements)
            design_payload = design.to_dict()
            analysis = model.analyze(design)
            design_record = DesignRecord.from_payload(
                design_payload,
                metadata={
                    "persistence_state": "not_persisted",
                    "source": "api_generation",
                },
            )
            revision = DesignRevisionRecord(
                design_id=design_record.design_id,
                requirement_snapshot=requirements,
                canonical_design_snapshot=design_payload,
                analysis_summary={
                    "result_class": analysis["result_class"],
                    "validity": analysis["validity"],
                    "metrics": analysis["metrics"],
                    "warnings": analysis["warnings"],
                },
            )
            return {
                "design": design_payload,
                "analysis": analysis,
                "model": registration.to_dict(),
                "design_hash": design_payload["design_hash"],
                "record": design_record.to_dict(),
                "revision": revision.to_dict(),
            }
        except EngineeringError as exc:
            raise map_engineering_error(exc) from exc
        except ValueError as exc:
            raise ApiException("INVALID_ENGINEERING_PARAMETER", str(exc), 400) from exc

    def validate_requirements(self, family: str, requirements: dict[str, Any]) -> dict[str, Any]:
        model = self.registry.create(family)
        try:
            calculated = model.calculate(requirements)
        except EngineeringError as exc:
            raise map_engineering_error(exc) from exc
        except ValueError as exc:
            raise ApiException("INVALID_ENGINEERING_PARAMETER", str(exc), 400) from exc
        return {
            "is_valid": True,
            "antenna_type": family,
            "normalized": calculated,
            "model": self.registry.get_registration(family).to_dict(),
            "warnings": [],
        }
