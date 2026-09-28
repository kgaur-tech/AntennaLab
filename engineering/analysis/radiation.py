"""Deterministic analytical radiation helpers for early AntennaLab analysis."""

from __future__ import annotations

import math


def half_wave_dipole_pattern(theta_deg: float) -> float:
    """Normalized E-plane power pattern for a center-fed thin half-wave dipole.

    The expression is proportional to
    (cos((pi / 2) * cos(theta)) / sin(theta))^2 and normalized to 1.0 at
    broadside. Values at the dipole axis are defined by the limiting null.
    """
    theta_rad = math.radians(theta_deg)
    sin_theta = math.sin(theta_rad)
    if abs(sin_theta) < 1e-12:
        return 0.0
    field = math.cos((math.pi / 2.0) * math.cos(theta_rad)) / sin_theta
    return field * field


def monopole_over_ground_pattern(theta_deg: float) -> float:
    """Normalized elevation power pattern for an ideal quarter-wave monopole.

    This uses the same upper-hemisphere shape as the corresponding half-wave
    dipole image model. Angles outside 0-90 degrees are unsupported here.
    """
    if theta_deg < 0.0 or theta_deg > 90.0:
        return 0.0
    return half_wave_dipole_pattern(theta_deg)


def azimuth_pattern(theta_deg: float, gain_db: float, beamwidth_deg: float) -> float:
    """Return a simple analytical far-field scalar for a directional pattern."""
    theta_rad = math.radians(theta_deg)
    beamwidth_rad = math.radians(beamwidth_deg)
    envelope = math.cos(theta_rad / beamwidth_rad) ** 2
    gain_linear = 10.0 ** (gain_db / 10.0)
    return gain_linear * max(0.0, envelope)


def polar_sample_set(gain_db: float, beamwidth_deg: float, sample_count: int = 36) -> list[dict[str, float]]:
    samples: list[dict[str, float]] = []
    for index in range(sample_count):
        theta_deg = (360.0 / sample_count) * index
        value = azimuth_pattern(theta_deg, gain_db, beamwidth_deg)
        samples.append({"angle_deg": theta_deg, "strength": value})
    return samples


def normalized_pattern_samples(pattern: str, sample_count: int = 181) -> list[dict[str, float]]:
    if sample_count < 2:
        raise ValueError("sample_count must be at least 2.")

    samples: list[dict[str, float]] = []
    if pattern == "half_wave_dipole_e_plane":
        max_angle = 180.0
        evaluator = half_wave_dipole_pattern
    elif pattern == "monopole_upper_hemisphere":
        max_angle = 90.0
        evaluator = monopole_over_ground_pattern
    else:
        raise ValueError(f"Unsupported analytical pattern: {pattern}.")

    for index in range(sample_count):
        angle = (max_angle / (sample_count - 1)) * index
        samples.append({"angle_deg": angle, "normalized_response": evaluator(angle)})
    return samples
