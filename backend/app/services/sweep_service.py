"""Bounded deterministic sweeps and grid-search ranking over internal analysis."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from json import dumps
from typing import Any, Literal
from uuid import uuid5, NAMESPACE_URL

from backend.app.core.errors import ApiException
from backend.app.repositories.design_repository import DesignRepository, design_repository
from backend.app.services.model_registry import AntennaModelRegistry, model_registry

MAX_CANDIDATES = 101
ALGORITHM = {"name": "deterministic-grid-search", "version": "v1"}


class SweepService:
    def __init__(self, repository: DesignRepository | None = None, registry: AntennaModelRegistry | None = None) -> None:
        self.repository = repository or design_repository
        self.registry = registry or model_registry
        self._cache: dict[str, dict[str, Any]] = {}

    def sweep(self, design_id: str, path: str, start: float, stop: float, step: float, metric: str) -> dict[str, Any]:
        design = self.repository.get(design_id)
        if design is None: raise ApiException("DESIGN_NOT_FOUND", "The requested design was not found.", 404, "design_id")
        values = self._range(start, stop, step)
        cache_key = sha256(dumps({"design": design, "path": path, "start": start, "stop": stop, "step": step, "metric": metric}, sort_keys=True).encode()).hexdigest()
        if cache_key in self._cache: return {**deepcopy(self._cache[cache_key]), "cache_hit": True}
        points: list[dict[str, Any]] = []
        for value in values:
            try:
                parameters = deepcopy(design["parameters"])
                if path == "frequency_hz":
                    parameters["frequency_hz"] = value
                else:
                    self._set_path(parameters, path, value)
                parameters["frequency_hz"] = design["frequency_hz"]
                if path == "frequency_hz":
                    parameters["frequency_hz"] = value
                model = self.registry.create(str(design["family"]))
                candidate = model.generate_design(parameters)
                analysis = model.analyze(candidate)
                if metric not in analysis["metrics"]:
                    raise ValueError(f"Metric '{metric}' is not available from the {design['family']} analysis model.")
                points.append({"value": value, "status": "COMPLETED", "metrics": analysis["metrics"], "analysis": analysis, "parameters": parameters})
            except (ValueError, KeyError) as exc:
                points.append({"value": value, "status": "INVALID", "errors": [str(exc)]})
        successful = [point for point in points if point["status"] == "COMPLETED"]
        result = {"sweep_id": str(uuid5(NAMESPACE_URL, cache_key)), "status": "COMPLETED" if len(successful) == len(points) else "PARTIAL", "cache_hit": False, "input_hash": cache_key, "base_design_id": design_id, "model_version": design["model_version"], "parameter": {"path": path, "unit": "m", "start": start, "stop": stop, "step": step}, "metric": metric, "points": points, "warnings": ["Sweep points are calculated by the registered internal model; unavailable metrics are not inferred."], "computation": {"candidate_count": len(points), "successful_count": len(successful), "failed_count": len(points) - len(successful), "cached_count": 0}}
        self._cache[cache_key] = deepcopy(result)
        return result

    def optimize(self, design_id: str, path: str, start: float, stop: float, step: float, metric: str, direction: Literal["maximize", "minimize"]) -> dict[str, Any]:
        sweep = self.sweep(design_id, path, start, stop, step, metric)
        feasible = [point for point in sweep["points"] if point["status"] == "COMPLETED"]
        if not feasible: return {"status": "FAILED", "base_design_id": design_id, "algorithm": ALGORITHM, "candidates": [], "best_candidates": [], "feasible_count": 0, "infeasible_count": len(sweep["points"])}
        ordered = sorted(feasible, key=lambda point: float(point["metrics"][metric]), reverse=direction == "maximize")
        best = ordered[0]
        return {"optimization_id": str(uuid5(NAMESPACE_URL, sweep["input_hash"] + direction)), "status": "COMPLETED", "base_design_id": design_id, "algorithm": ALGORITHM, "objective": {"metric": metric, "direction": direction}, "candidates": ordered, "best_candidates": [best], "feasible_count": len(feasible), "infeasible_count": len(sweep["points"]) - len(feasible), "warning": "Highest objective score among evaluated feasible candidates; not a global optimum claim."}

    @staticmethod
    def _range(start: float, stop: float, step: float) -> list[float]:
        if step <= 0 or stop < start: raise ApiException("INVALID_SWEEP_RANGE", "Sweep requires stop >= start and a positive step.", 422)
        count = int(round((stop - start) / step)) + 1
        if count > MAX_CANDIDATES: raise ApiException("SWEEP_LIMIT_EXCEEDED", f"A sweep may contain at most {MAX_CANDIDATES} candidates.", 422)
        return [round(start + index * step, 12) for index in range(count)]

    @staticmethod
    def _set_path(parameters: dict[str, Any], path: str, value: float) -> None:
        if "[" in path and path.endswith("]"):
            name, index_text = path[:-1].split("[", 1); index = int(index_text)
            if name not in parameters or not isinstance(parameters[name], list) or index < 0 or index >= len(parameters[name]): raise ValueError(f"Editable parameter path '{path}' does not exist.")
            parameters[name][index] = value
        elif path in parameters and isinstance(parameters[path], (int, float)):
            parameters[path] = value
        else: raise ValueError(f"Editable parameter path '{path}' does not exist.")


sweep_service = SweepService()
