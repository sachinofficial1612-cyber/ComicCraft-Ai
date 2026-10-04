import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["backend"] is True
    assert "database" in data

def test_ai_health_check():
    response = client.get("/api/health/ai")
    assert response.status_code == 200
    data = response.json()
    assert "configured" in data
    assert "text_model" in data

def test_create_and_get_project():
    payload = {
        "original_prompt": "A heroic cat saves the town from giant mice.",
        "character_name": "Felix",
        "setting": "Metropolis",
        "tone": "Humorous",
        "art_style": "Cartoon",
        "panel_count": "4"
    }
    create_resp = client.post("/api/projects", json=payload)
    assert create_resp.status_code == 201
    proj_data = create_resp.json()
    assert proj_data["character_name"] == "Felix"
    assert proj_data["panel_count"] == 4
    project_id = proj_data["id"]

    get_resp = client.get(f"/api/projects/{project_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == project_id

def test_list_projects():
    response = client.get("/api/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_demo_project_endpoint():
    response = client.post("/api/projects/demo")
    assert response.status_code == 200
    demo_data = response.json()
    assert demo_data["character_name"] == "Free"
    assert len(demo_data["panels"]) > 0
