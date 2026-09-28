from __future__ import annotations

from typing import Any

from engineering.core.exceptions import EngineeringError

from backend.app.core.errors import ApiException, map_engineering_error
from backend.app.models.design import DesignRecord, DesignRevisionRecord
from backend.app.repositories.design_repository import DesignRepository, design_repository
from backend.app.services.model_registry import model_registry


class DesignService:
    """Coordinates deterministic design generation for the supported antenna families."""

    def __init__(self, repository: DesignRepository | None = None) -> None:
        self.registry = model_registry
        self.repository = repository or design_repository

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
            self.repository.save(design_payload)
            saved_revision = self.repository.save_revision(revision.to_dict())
            return {
                "design": design_payload,
                "analysis": analysis,
                "model": registration.to_dict(),
                "design_hash": design_payload["design_hash"],
                "record": design_record.to_dict(),
                "revision": saved_revision,
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

    def get(self, design_id: str) -> dict[str, Any]:
        design = self.repository.get(design_id)
        if design is None:
            raise ApiException("DESIGN_NOT_FOUND", "The requested design was not found.", 404, "design_id")
        return design

    def update(self, design_id: str, parameters: dict[str, Any]) -> dict[str, Any]:
        current = self.get(design_id)
        merged = {**current["parameters"], **parameters}
        merged["frequency_hz"] = parameters.get("frequency_hz", current["frequency_hz"])
        result = self.generate(str(current["family"]), merged)
        result["design"]["design_id"] = design_id
        result["record"]["design_id"] = design_id
        result["record"]["canonical_design"] = result["design"]
        result["revision"]["design_id"] = design_id
        result["revision"]["canonical_design_snapshot"] = result["design"]
        if result["analysis"].get("geometry_reference"):
            result["analysis"]["geometry_reference"]["design_id"] = design_id
        self.repository.save(result["design"])
        return result

    def create_revision(self, design_id: str) -> dict[str, Any]:
        design = self.get(design_id)
        revision = DesignRevisionRecord(
            design_id=design_id,
            requirement_snapshot={},
            canonical_design_snapshot=design,
            analysis_summary={"state": "not_recomputed"},
        )
        return self.repository.save_revision(revision.to_dict())
