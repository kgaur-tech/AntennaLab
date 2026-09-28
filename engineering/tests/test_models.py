import pytest

from engineering.antennas.dipole.dipole import DipoleModel
from engineering.antennas.monopole.monopole import MonopoleModel
from engineering.antennas.yagi_uda.yagi_uda import YagiUdaModel


def test_dipole_design_has_expected_dimensions() -> None:
    design = DipoleModel().generate_design({"frequency_hz": 2.4e9})
    assert design.family == "dipole"
    assert design.model_version == "dipole-v1"
    assert design.dimensions_m["total_length"] > 0
    assert design.dimensions_m["total_length"] == pytest.approx(design.parameters["wavelength_m"] / 2.0)


def test_monopole_design_is_quarter_wave() -> None:
    design = MonopoleModel().generate_design({"frequency_hz": 2.4e9})
    assert design.family == "monopole"
    assert design.dimensions_m["total_length"] > 0
    assert design.dimensions_m["total_length"] == pytest.approx(design.parameters["wavelength_m"] / 4.0)


def test_yagi_uda_design_has_directional_geometry() -> None:
    design = YagiUdaModel().generate_design({"frequency_hz": 2.4e9})
    assert design.family == "yagi_uda"
    assert design.model_version == "yagi-uda-v1"
    assert design.dimensions_m["director_1_length"] > 0
    assert len(design.dimensions_m["director_lengths"]) == 3


def test_yagi_uda_supports_individual_director_mutability() -> None:
    design = YagiUdaModel().generate_design({
        "frequency_hz": 915e6,
        "director_count": 4,
        "director_lengths_m": [0.14, 0.139, 0.138, 0.137],
        "element_spacings_m": [0.06, 0.05, 0.051, 0.052, 0.053],
    })

    assert design.dimensions_m["director_3_length"] == pytest.approx(0.138)
    director_3 = [element for element in design.geometry.elements if element.name == "director_3"][0]
    assert director_3.length_m == pytest.approx(0.138)
    assert director_3.metadata["parameter"] == "director_3_length"
