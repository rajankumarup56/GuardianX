import time
from fastapi.testclient import TestClient
from app.main import app
from app.services.security_validator import SecurityValidator

client = TestClient(app)


def test_security_evaluate_allows_trusted_owner_command():
    response = client.post(
        "/api/v1/security/evaluate",
        json={
            "user": {
                "user_id": "user-test-001",
                "username": "testuser",
                "role": "VIEWER",
                "active": True,
            },
            "device": {
                "device_id": "device-test-001",
                "device_name": "Test Drone",
                "device_type": "drone",
                "owner_id": "user-test-001",
                "trusted": True,
                "active": True,
                "risk_level": "LOW",
            },
            "command": {
                "command_id": "cmd-test-001",
                "device_id": "device-test-001",
                "issued_by": "user-test-001",
                "command_type": "STATUS_CHECK",
                "parameters": {},
            },
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "BLOCK"
    assert data["risk_level"] == "LOW"
    assert data["risk_score"] == 20


def test_security_evaluate_blocks_untrusted_device():
    response = client.post(
        "/api/v1/security/evaluate",
        json={
            "user": {
                "user_id": "user-test-002",
                "username": "testuser2",
                "role": "SECURITY_ADMIN",
                "active": True,
            },
            "device": {
                "device_id": "device-test-002",
                "device_name": "Untrusted Drone",
                "device_type": "drone",
                "owner_id": "user-test-002",
                "trusted": False,
                "active": True,
                "risk_level": "LOW",
            },
            "command": {
                "command_id": "cmd-test-002",
                "device_id": "device-test-002",
                "issued_by": "user-test-002",
                "command_type": "STATUS_CHECK",
                "parameters": {},
            },
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["decision"] == "BLOCK"
    assert data["risk_level"] == "HIGH"
    assert data["risk_score"] == 50


def test_telemetry_normalize_removes_unknown_fields():
    response = client.post(
        "/api/v1/telemetry/normalize",
        json={
            "battery": 87,
            "altitude": 42.5,
            "speed": 12.3,
            "latitude": 25.5941,
            "longitude": 84.9912,
            "flight_mode": "OFFBOARD",
            "unknown_field": "should_be_removed",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["battery"] == 87
    assert data["altitude"] == 42.5
    assert data["flight_mode"] == "OFFBOARD"
    assert "unknown_field" not in data


def test_telemetry_evaluate_returns_critical_risk():
    response = client.post(
        "/api/v1/telemetry/evaluate",
        json={
            "battery": 15,
            "temperature": 85,
            "speed": 30,
            "altitude": 42.5,
            "unknown_field": "should_be_removed",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "CRITICAL"
    assert data["risk_score"] == 80
    assert data["telemetry"]["battery"] == 15
    assert data["telemetry"]["temperature"] == 85
    assert data["telemetry"]["speed"] == 30
    assert data["telemetry"]["altitude"] == 42.5
    assert "unknown_field" not in data["telemetry"]


def test_security_validator_bounds():
    validator = SecurityValidator()
    ok, msg = validator.validate_telemetry_bounds({"speed": 50.0, "altitude": 100.0})
    assert ok is True

    ok, msg = validator.validate_telemetry_bounds({"speed": 9999.0, "altitude": 100.0})
    assert ok is False
    assert "speed" in msg


def test_replay_attack_detection():
    validator = SecurityValidator()
    ok, _ = validator.validate_timestamp_drift(time.time())
    assert ok is True

    ok, msg = validator.validate_timestamp_drift(time.time() - 100)
    assert ok is False
    assert "Replay attack" in msg