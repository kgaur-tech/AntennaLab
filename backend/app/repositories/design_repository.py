from __future__ import annotations

from copy import deepcopy
from typing import Any


class DesignRepository:
    """Persisted storage contract for antenna designs and revisions."""

    def __init__(self) -> None:
        self._designs: dict[str, dict[str, Any]] = {}
        self._revisions: dict[str, list[dict[str, Any]]] = {}

    def save(self, design: dict[str, Any]) -> dict[str, Any]:
        self._designs[str(design["design_id"])] = deepcopy(design)
        return deepcopy(design)

    def get(self, design_id: str) -> dict[str, Any] | None:
        design = self._designs.get(design_id)
        return deepcopy(design) if design else None

    def save_revision(self, revision: dict[str, Any]) -> dict[str, Any]:
        revisions = self._revisions.setdefault(str(revision["design_id"]), [])
        stored = deepcopy(revision)
        stored["revision_number"] = len(revisions) + 1
        revisions.append(stored)
        return deepcopy(stored)

    def list_revisions(self, design_id: str) -> list[dict[str, Any]]:
        return deepcopy(self._revisions.get(design_id, []))

    def get_revision(self, design_id: str, revision_number: int) -> dict[str, Any] | None:
        for revision in self._revisions.get(design_id, []):
            if revision["revision_number"] == revision_number:
                return deepcopy(revision)
        return None

    def list_recent(self) -> list[dict[str, Any]]:
        return [deepcopy(design) for design in self._designs.values()]


design_repository = DesignRepository()
