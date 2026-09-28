from backend.app.repositories.design_repository import DesignRepository
from backend.app.services.design_service import DesignService
from backend.app.services.history_service import HistoryService


def test_revision_comparison_and_datasheet_are_derived_from_immutable_snapshots() -> None:
    repository = DesignRepository()
    service = DesignService(repository=repository)
    design = service.generate("yagi_uda", {"frequency_hz": 915e6, "director_count": 3})["design"]
    original = design["parameters"]["director_lengths_m"]
    service.update(design["design_id"], {"director_lengths_m": [original[0], original[1], 0.14]})
    service.create_revision(design["design_id"])
    history = HistoryService(repository=repository)

    comparison = history.compare(design["design_id"], 1, 2)
    assert any(change["path"] == "director_lengths_m[2]" for change in comparison["parameter_changes"])
    sheet = history.datasheet(design["design_id"], 1)
    assert sheet["reproducibility"]["design_id"] == design["design_id"]
    assert sheet["document_type"] == "AntennaLab Engineering Design Datasheet"
