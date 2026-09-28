from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_design_lifecycle_updates_yagi_geometry_and_saves_revision() -> None:
    created = client.post("/api/v1/designs", json={"antenna_type": "yagi_uda", "frequency": 915, "frequency_unit": "MHz", "director_count": 3}).json()["data"]
    design_id = created["design"]["design_id"]
    original_directors = created["design"]["parameters"]["director_lengths_m"]

    updated = client.patch(f"/api/v1/designs/{design_id}", json={"parameters": {"director_lengths_m": [original_directors[0], original_directors[1], 0.14]}})
    assert updated.status_code == 200
    updated_design = updated.json()["data"]["design"]
    assert updated_design["design_id"] == design_id
    assert updated_design["parameters"]["director_lengths_m"][:2] == original_directors[:2]
    assert updated_design["parameters"]["director_lengths_m"][2] == 0.14

    validated = client.post(f"/api/v1/designs/{design_id}/validate")
    assert validated.status_code == 200
    revision = client.post(f"/api/v1/designs/{design_id}/revisions")
    assert revision.status_code == 200
    assert revision.json()["data"]["revision_number"] >= 2
