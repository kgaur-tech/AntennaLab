import pytest
from typing import Any

from engineering.antennas.base import AntennaModel
from engineering.antennas.dipole.dipole import DipoleModel
from engineering.antennas.monopole.monopole import MonopoleModel
from engineering.antennas.yagi_uda.yagi_uda import YagiUdaModel

def test_requirement_to_design_to_analysis_pipeline() -> None:
    models: dict[str, AntennaModel] = {
        "dipole": DipoleModel(),
        "monopole": MonopoleModel(),
        "yagi_uda": YagiUdaModel(),
    }

    for family, model in models.items():
        design = model.generate_design({"frequency_hz": 2.4e9})
        analysis = model.evaluate(design)
        assert design.family == family
        assert design.frequency_hz > 0
        assert analysis["model_type"] == family
        assert analysis["result_class"] == "CALCULATED"
        assert analysis["geometry_reference"]["design_id"] == design.design_id

def test_design_generation_is_deterministic() -> None:
    model = YagiUdaModel()
    requirements: dict[str, Any] = {
        "frequency_hz": 915e6,
        "director_count": 3,
        "director_lengths_m": [0.145, 0.143, 0.141],
        "element_spacings_m": [0.065, 0.055, 0.055, 0.055],
    }

    first = model.generate_design(requirements)
    second = model.generate_design(requirements)

    assert first.to_dict() == second.to_dict()


def test_phase_one_pipeline_normalizes_validates_designs_and_analyzes() -> None:
    model = DipoleModel()
    design = model.generate_design({"frequency_hz": 915.0, "frequency_unit": "mhz"})
    analysis = model.analyze(design, {"sample_count": 19})

    assert design.frequency_hz == 915e6
    assert design.geometry is not None
    assert len(design.geometry.elements) == 2
    assert analysis["result_class"] == "CALCULATED"
    assert analysis["metrics"]["wavelength_m"] == pytest.approx(0.327642, rel=1e-5)
    assert analysis["plots"][0]["data"]
