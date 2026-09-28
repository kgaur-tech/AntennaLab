from backend.app.repositories.design_repository import DesignRepository
from backend.app.services.design_service import DesignService
from backend.app.services.sweep_service import SweepService


def test_yagi_director_sweep_is_deterministic_and_isolates_other_directors() -> None:
    repository = DesignRepository()
    design = DesignService(repository=repository).generate("yagi_uda", {"frequency_hz": 915e6, "director_count": 3})["design"]
    service = SweepService(repository=repository)
    first = service.sweep(design["design_id"], "director_lengths_m[2]", 0.13, 0.14, 0.005, "boom_length_m")
    second = service.sweep(design["design_id"], "director_lengths_m[2]", 0.13, 0.14, 0.005, "boom_length_m")
    assert len(first["points"]) == 3
    assert second["cache_hit"] is True
    assert first["points"][0]["parameters"]["director_lengths_m"][:2] == design["parameters"]["director_lengths_m"][:2]


def test_sweep_limit_and_optimization_ranking() -> None:
    repository = DesignRepository()
    design = DesignService(repository=repository).generate("dipole", {"frequency_hz": 915e6})["design"]
    service = SweepService(repository=repository)
    result = service.optimize(design["design_id"], "frequency_hz", 800e6, 900e6, 50e6, "wavelength_m", "minimize")
    assert result["best_candidates"][0]["value"] == 900e6
