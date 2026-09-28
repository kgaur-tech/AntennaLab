from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from engineering.antennas.base import AntennaModel
from engineering.antennas.dipole.dipole import DipoleModel
from engineering.antennas.monopole.monopole import MonopoleModel
from engineering.antennas.yagi_uda.yagi_uda import YagiUdaModel

from backend.app.core.errors import UnsupportedModelException


@dataclass(frozen=True)
class ModelRegistration:
    model_id: str
    model_version: str
    capabilities: tuple[str, ...]
    factory: Callable[[], AntennaModel]

    def to_dict(self) -> dict[str, object]:
        return {
            "model": self.model_id,
            "model_version": self.model_version,
            "capabilities": list(self.capabilities),
        }


class AntennaModelRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, ModelRegistration] = {
            "dipole": ModelRegistration(
                model_id="dipole",
                model_version="dipole-v1",
                capabilities=("canonical_design", "geometry", "analytical_pattern"),
                factory=DipoleModel,
            ),
            "monopole": ModelRegistration(
                model_id="monopole",
                model_version="monopole-v1",
                capabilities=("canonical_design", "geometry", "analytical_pattern"),
                factory=MonopoleModel,
            ),
            "yagi_uda": ModelRegistration(
                model_id="yagi_uda",
                model_version="yagi-uda-v1",
                capabilities=("canonical_design", "geometry", "dimensional_analysis"),
                factory=YagiUdaModel,
            ),
        }

    def list_models(self) -> list[dict[str, object]]:
        return [registration.to_dict() for registration in self._registry.values()]

    def get_registration(self, model_id: str) -> ModelRegistration:
        if model_id not in self._registry:
            raise UnsupportedModelException(model_id)
        return self._registry[model_id]

    def create(self, model_id: str) -> AntennaModel:
        return self.get_registration(model_id).factory()

    def supported_model_ids(self) -> set[str]:
        return set(self._registry)


model_registry = AntennaModelRegistry()
