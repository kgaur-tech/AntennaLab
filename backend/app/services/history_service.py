"""Immutable revision history, comparison, and engineering datasheet payloads."""

from __future__ import annotations

from typing import Any

from backend.app.core.errors import ApiException
from backend.app.repositories.design_repository import DesignRepository, design_repository


class HistoryService:
    def __init__(self, repository: DesignRepository | None = None) -> None:
        self.repository = repository or design_repository

    def list_revisions(self, design_id: str) -> list[dict[str, Any]]:
        if self.repository.get(design_id) is None:
            raise ApiException("DESIGN_NOT_FOUND", "The requested design was not found.", 404, "design_id")
        return self.repository.list_revisions(design_id)

    def compare(self, design_id: str, left: int, right: int) -> dict[str, Any]:
        first = self.repository.get_revision(design_id, left)
        second = self.repository.get_revision(design_id, right)
        if first is None or second is None:
            raise ApiException("REVISION_NOT_FOUND", "One or both requested revisions were not found.", 404, "revision")
        old = first["canonical_design_snapshot"]
        new = second["canonical_design_snapshot"]
        return {"design_id": design_id, "left_revision": first, "right_revision": second, "parameter_changes": self._diff(old["parameters"], new["parameters"]), "metric_comparison": self._metric_comparison(first["analysis_summary"], second["analysis_summary"])}

    def datasheet(self, design_id: str, revision_number: int | None = None) -> dict[str, Any]:
        design = self.repository.get(design_id)
        if design is None: raise ApiException("DESIGN_NOT_FOUND", "The requested design was not found.", 404, "design_id")
        revision = self.repository.get_revision(design_id, revision_number) if revision_number else (self.repository.list_revisions(design_id)[-1] if self.repository.list_revisions(design_id) else None)
        snapshot = revision["canonical_design_snapshot"] if revision else design
        return {"document_type": "AntennaLab Engineering Design Datasheet", "design": snapshot, "revision": revision, "analysis": revision["analysis_summary"] if revision else {"status": "not_available"}, "reproducibility": {"design_id": design_id, "design_hash": snapshot["design_hash"], "model_version": snapshot["model_version"], "revision_number": revision["revision_number"] if revision else None}}

    def _diff(self, old: dict[str, Any], new: dict[str, Any], prefix: str = "") -> list[dict[str, Any]]:
        changes: list[dict[str, Any]] = []
        for key in sorted(set(old) | set(new)):
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(old.get(key), list) and isinstance(new.get(key), list):
                for index, (before, after) in enumerate(zip(old[key], new[key])):
                    if before != after: changes.append({"path": f"{path}[{index}]", "old": before, "new": after})
            elif old.get(key) != new.get(key): changes.append({"path": path, "old": old.get(key), "new": new.get(key)})
        return changes

    @staticmethod
    def _metric_comparison(old: dict[str, Any], new: dict[str, Any]) -> list[dict[str, Any]]:
        old_metrics, new_metrics = old.get("metrics", {}), new.get("metrics", {})
        return [{"metric": key, "left": old_metrics.get(key), "right": new_metrics.get(key), "status": "AVAILABLE" if key in old_metrics and key in new_metrics else "NOT_AVAILABLE"} for key in sorted(set(old_metrics) | set(new_metrics))]


history_service = HistoryService()
