from backend.app.repositories.design_repository import DesignRepository
from backend.app.services.analysis_service import AnalysisService
from backend.app.services.design_service import DesignService


def test_dipole_analysis_is_deterministic_cached_and_has_normalized_pattern() -> None:
    repository = DesignRepository()
    design = DesignService(repository=repository).generate("dipole", {"frequency_hz": 915e6})["design"]
    service = AnalysisService(repository=repository)

    first = service.analyze(design["design_id"], {"sample_count": 19})
    second = service.analyze(design["design_id"], {"sample_count": 19})

    assert first["result_class"] == "CALCULATED"
    assert first["analysis_type"] == "fast_analytical"
    assert first["input_hash"] == second["input_hash"]
    assert second["cache_hit"] is True
    samples = first["plots"][0]["data"]
    assert len(samples) == 19
    assert samples[0]["normalized_response"] == 0.0
    assert max(item["normalized_response"] for item in samples) == 1.0
    assert "vswr" not in first["metrics"]


def test_relevant_design_change_changes_analysis_input_hash() -> None:
    repository = DesignRepository()
    service = DesignService(repository=repository)
    design = service.generate("dipole", {"frequency_hz": 915e6})["design"]
    analysis = AnalysisService(repository=repository)
    original = analysis.analyze(design["design_id"])
    updated = service.update(design["design_id"], {"frequency_hz": 868e6})["design"]
    revised = analysis.analyze(updated["design_id"])

    assert original["input_hash"] != revised["input_hash"]
