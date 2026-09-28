from backend.app.models.requirement import AntennaRequirement
from backend.app.services.explainable_recommendation_service import ENGINE_VERSION, ExplainableRecommendationService


def test_directionality_is_a_hard_constraint_and_returns_exclusions() -> None:
    result = ExplainableRecommendationService().recommend(AntennaRequirement(
        application="rocket telemetry", frequency_hz=915e6, polarization="linear",
        directionality="directional", is_directional=True, max_dimension_m=1.0,
    ))

    assert result["engine_version"] == ENGINE_VERSION
    assert result["recommended"][0]["family"] == "yagi_uda"
    excluded = {item["family"]: item for item in result["excluded_candidates"]}
    assert {"dipole", "monopole"} <= set(excluded)
    assert any(item["reason_code"] == "DIRECTIONALITY_MISMATCH" for item in excluded["dipole"]["hard_constraints"])


def test_recommendation_is_deterministic_and_marks_unknown_criteria() -> None:
    requirement = AntennaRequirement(application="custom", frequency_hz=915e6, polarization="linear", directionality="no_preference")
    first = ExplainableRecommendationService().recommend(requirement)
    second = ExplainableRecommendationService().recommend(requirement)

    assert first == second
    components = first["recommended"][0]["score_components"]
    assert any(item["reason_code"] == "GAIN_NOT_EVALUATED" and item["status"] == "UNSUPPORTED" for item in components)


def test_restrictive_dimension_can_exclude_every_candidate() -> None:
    result = ExplainableRecommendationService().recommend(AntennaRequirement(
        application="custom", frequency_hz=915e6, polarization="linear", max_dimension_m=0.001,
    ))

    assert result["recommended"] == []
    assert len(result["excluded_candidates"]) == 3
