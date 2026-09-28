from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.design_service import DesignService

client = TestClient(app, raise_server_exceptions=False)


def test_model_listing_returns_capabilities() -> None:
    response = client.get("/api/v1/models")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    models = body["data"]["models"]
    assert {model["model"] for model in models} == {"dipole", "monopole", "yagi_uda"}
    assert any("geometry" in model["capabilities"] for model in models)


def test_create_design_returns_canonical_contract() -> None:
    response = client.post(
        "/api/v1/designs",
        json={"antenna_type": "dipole", "frequency": 915, "frequency_unit": "MHz"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert data["design"]["family"] == "dipole"
    assert data["design"]["frequency_hz"] == 915e6
    assert data["analysis"]["result_class"] == "CALCULATED"
    assert data["model"]["model_version"] == "dipole-v1"
    assert data["design_hash"] == data["design"]["design_hash"]
    assert data["record"]["design_id"] == data["design"]["design_id"]
    assert data["revision"]["revision_number"] == 1


def test_requirement_validation_returns_normalized_payload_without_design_generation() -> None:
    response = client.post(
        "/api/v1/requirements/validate",
        json={"antenna_type": "monopole", "frequency": 0.915, "frequency_unit": "GHz"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["is_valid"] is True
    assert body["data"]["normalized"]["frequency_hz"] == pytest.approx(915e6)
    assert body["data"]["model"]["model"] == "monopole"


def test_recommendations_use_the_standard_api_envelope() -> None:
    response = client.post(
        "/api/v1/requirements/recommend",
        json={
            "application": "IoT sensor node",
            "frequency": 915,
            "frequency_unit": "MHz",
            "is_directional": False,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["recommendations"]


def test_missing_required_field_returns_structured_error() -> None:
    response = client.post("/api/v1/designs", json={"frequency": 915, "frequency_unit": "MHz"})

    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["field"] == "antenna_type"


def test_invalid_frequency_returns_structured_error() -> None:
    response = client.post(
        "/api/v1/designs",
        json={"antenna_type": "dipole", "frequency": -915, "frequency_unit": "MHz"},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_invalid_unit_returns_structured_error() -> None:
    response = client.post(
        "/api/v1/designs",
        json={"antenna_type": "dipole", "frequency": 915, "frequency_unit": "RPM"},
    )

    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["field"] == "frequency_unit"


def test_unsupported_antenna_type_returns_structured_error() -> None:
    response = client.post(
        "/api/v1/designs",
        json={"antenna_type": "patch", "frequency": 915, "frequency_unit": "MHz"},
    )

    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "UNSUPPORTED_ANTENNA_TYPE"
    assert body["error"]["field"] == "antenna_type"


def test_invalid_dimension_returns_structured_error() -> None:
    response = client.post(
        "/api/v1/designs",
        json={
            "antenna_type": "yagi_uda",
            "frequency": 915,
            "frequency_unit": "MHz",
            "element_radius_m": -0.001,
        },
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_equivalent_units_generate_same_design_hash() -> None:
    service = DesignService()

    mhz_design = service.generate("dipole", {"frequency_hz": 915, "frequency_unit": "MHz"})
    ghz_design = service.generate("dipole", {"frequency_hz": 0.915, "frequency_unit": "GHz"})
    hz_design = service.generate("dipole", {"frequency_hz": 915000000.0})

    assert mhz_design["design_hash"] == ghz_design["design_hash"] == hz_design["design_hash"]
    assert mhz_design["design"] == ghz_design["design"] == hz_design["design"]


def test_identical_requirements_are_deterministic() -> None:
    service = DesignService()
    first = service.generate("yagi_uda", {"frequency_hz": 915e6, "director_count": 3})
    second = service.generate("yagi_uda", {"frequency_hz": 915e6, "director_count": 3})

    assert first["design"] == second["design"]
    assert first["analysis"] == second["analysis"]
    assert first["design_hash"] == second["design_hash"]


def test_unexpected_internal_exception_returns_safe_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def explode(_: str):
        raise RuntimeError("secret internal detail")

    monkeypatch.setattr("backend.app.services.model_registry.model_registry.create", explode)

    response = client.post(
        "/api/v1/designs",
        json={"antenna_type": "dipole", "frequency": 915, "frequency_unit": "MHz"},
    )

    assert response.status_code == 500
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "INTERNAL_SERVER_ERROR"
    assert "secret" not in body["error"]["message"]
