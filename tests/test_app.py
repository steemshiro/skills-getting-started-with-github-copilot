import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_remove_participant():
    # Use a unique email to avoid conflicts
    test_email = "pytestuser@mergington.edu"
    activity = "Chess Club"

    # Remove if already present
    client.post(f"/activities/{activity}/remove", params={"email": test_email})

    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

    # Remove participant
    response = client.post(f"/activities/{activity}/remove", params={"email": test_email})
    assert response.status_code == 200
    assert f"Removed {test_email}" in response.json()["message"]

    # Remove again should fail
    response = client.post(f"/activities/{activity}/remove", params={"email": test_email})
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
