import math

import pytest

from engineering.core.constants.physics import C0, ETA_0
from engineering.core.exceptions import InvalidEngineeringParameter
from engineering.core.math.wave import wavelength_m
from engineering.core.units.angle import deg_to_rad
from engineering.core.units.frequency import ghz_to_hz, mhz_to_hz, normalize_frequency
from engineering.core.units.length import cm_to_m, m_to_cm, m_to_mm, mm_to_m, normalize_length


def test_speed_of_light_and_wave_impedance_are_defined() -> None:
    assert C0 > 0
    assert ETA_0 > 0


def test_frequency_conversions_are_numeric_and_consistent() -> None:
    assert mhz_to_hz(1.0) == 1_000_000.0
    assert ghz_to_hz(1.0) == 1_000_000_000.0
    assert ghz_to_hz(1.0) == pytest.approx(1e9)
    assert mhz_to_hz(915.0) == pytest.approx(915e6)
    assert normalize_frequency(915.0, "MHz") == pytest.approx(915e6)


def test_length_conversions_are_numeric_and_consistent() -> None:
    assert mm_to_m(1000.0) == 1.0
    assert cm_to_m(100.0) == 1.0
    assert m_to_cm(1.0) == pytest.approx(100.0)
    assert m_to_mm(1.0) == pytest.approx(1000.0)
    assert normalize_length(1000.0, "mm") == pytest.approx(1.0)


def test_angle_conversion_is_consistent() -> None:
    assert deg_to_rad(180.0) == pytest.approx(math.pi)


def test_wavelength_is_positive_and_physical() -> None:
    assert wavelength_m(2.4e9) > 0
    assert wavelength_m(2.4e9) < 1.0


def test_915_mhz_wavelength_reference_case() -> None:
    assert wavelength_m(915e6) == pytest.approx(0.327642, rel=1e-5)


def test_invalid_units_and_non_physical_values_are_rejected() -> None:
    with pytest.raises(InvalidEngineeringParameter):
        normalize_frequency(1.0, "rpm")
    with pytest.raises(InvalidEngineeringParameter):
        normalize_length(1.0, "inch")
    with pytest.raises(InvalidEngineeringParameter):
        normalize_frequency(0.0, "hz")
    with pytest.raises(InvalidEngineeringParameter):
        normalize_length(-1.0, "m")
