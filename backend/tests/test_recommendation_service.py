from backend.app.models.requirement import AntennaRequirement
from backend.app.services.recommendation_service import RecommendationService


def test_requirement_recommendation_prefers_directional_high_gain() -> None:
    requirement = AntennaRequirement(
        application="rocket telemetry",
        frequency_hz=2.4e9,
        gain_db=10.0,
        polarization="linear",
        is_directional=True,
        max_dimension_m=0.45,
        target_impedance_ohms=50.0,
        environment="outdoor",
    )

    recommendations = RecommendationService().recommend(requirement)

    assert recommendations
    assert recommendations[0].family == "yagi_uda"
    assert any("directional" in reason.lower() for reason in recommendations[0].reasons)


def test_requirement_recommendation_is_simple_for_small_omnidirectional_use() -> None:
    requirement = AntennaRequirement(
        application="IoT sensor node",
        frequency_hz=915e6,
        gain_db=2.0,
        polarization="linear",
        is_directional=False,
        max_dimension_m=0.12,
        target_impedance_ohms=50.0,
        environment="indoor",
    )

    recommendations = RecommendationService().recommend(requirement)

    assert recommendations
    assert recommendations[0].family in {"dipole", "monopole"}
