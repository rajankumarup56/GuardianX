import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def admin_auth_headers():
    return {"Authorization": "Bearer admin-secret-token"}

def test_system_integrity_status_unauthorized():
    """Verify that unauthorized requests are blocked."""
    response = client.get("/api/v1/system/integrity-status")
    assert response.status_code in [401, 403, 404]  # Handles route check gracefully

def test_system_integrity_status_authorized(admin_auth_headers):
    """Verify that authorized admin requests return system integrity status."""
    response = client.get(
        "/api/v1/system/integrity-status",
        headers=admin_auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "tamper_status" in data
    assert data["tamper_status"] == "VALIDATED"
    assert "siem_chain_state" in data
    assert "risk_engine_config" in data