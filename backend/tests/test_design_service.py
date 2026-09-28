from backend.app.services.design_service import DesignService


def test_design_service_generates_supported_family() -> None:
    service = DesignService()
    design = service.generate("dipole", {"frequency_hz": 2.4e9})
    assert design["design"]["family"] == "dipole"
    assert design["design"]["dimensions_m"]["total_length"] > 0
    assert design["analysis"]["result_class"] == "CALCULATED"
