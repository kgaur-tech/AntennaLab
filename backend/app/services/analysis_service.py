"""Fast deterministic analysis lifecycle for canonical AntennaLab designs."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from json import dumps
from time import perf_counter
from typing import Any
from uuid import uuid5, NAMESPACE_URL

from backend.app.core.errors import ApiException
from backend.app.repositories.design_repository import DesignRepository, design_repository
from backend.app.services.model_registry import AntennaModelRegistry, model_registry


class AnalysisService:
    """Runs synchronous Tier 1 analyses and safely reuses identical results."""

    def __init__(self, repository: DesignRepository | None = None, registry: AntennaModelRegistry | None = None) -> None:
        self.repository = repository or design_repository
        self.registry = registry or model_registry
        self._cache: dict[str, dict[str, Any]] = {}
        self._by_id: dict[str, dict[str, Any]] = {}

    def analyze(self, design_id: str, settings: dict[str, Any] | None = None) -> dict[str, Any]:
        design = self.repository.get(design_id)
        if design is None:
            raise ApiException("DESIGN_NOT_FOUND", "The requested design was not found.", 404, "design_id")
        settings = settings or {}
        input_hash = self._input_hash(design, settings)
        if input_hash in self._cache:
            cached = deepcopy(self._cache[input_hash])
            cached["cache_hit"] = True
            return cached
        model = self.registry.create(str(design["family"]))
        generated = model.generate_design({**dict(design["parameters"]), "frequency_hz": design["frequency_hz"]})
        generated.design_id = design_id
        started = perf_counter()
        analysis = model.analyze(generated, settings)
        duration_ms = round((perf_counter() - started) * 1000, 3)
        analysis_id = str(uuid5(NAMESPACE_URL, f"{input_hash}:{analysis['model_version']}"))
        result = {
            "analysis_id": analysis_id,
            "design_id": design_id,
            "analysis_type": "fast_analytical",
            "status": "COMPLETED",
            "cache_hit": False,
            "input_hash": input_hash,
            "computed_at": datetime.now(timezone.utc).isoformat(),
            "duration_ms": duration_ms,
            **analysis,
        }
        self._cache[input_hash] = deepcopy(result)
        self._by_id[analysis_id] = deepcopy(result)
        return result

    def latest(self, design_id: str) -> dict[str, Any] | None:
        candidates = [value for value in self._by_id.values() if value["design_id"] == design_id]
        return deepcopy(candidates[-1]) if candidates else None

    def get(self, analysis_id: str) -> dict[str, Any]:
        result = self._by_id.get(analysis_id)
        if result is None:
            raise ApiException("ANALYSIS_NOT_FOUND", "The requested analysis was not found.", 404, "analysis_id")
        return deepcopy(result)

    @staticmethod
    def _input_hash(design: dict[str, Any], settings: dict[str, Any]) -> str:
        payload = {"family": design["family"], "model_version": design["model_version"], "frequency_hz": design["frequency_hz"], "parameters": design["parameters"], "settings": settings}
        return sha256(dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


analysis_service = AnalysisService()
