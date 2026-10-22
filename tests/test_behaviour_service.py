from app.models.behaviour import BehaviourProfile
from app.services.behaviour_service import BehaviourService


def test_normal_behaviour_has_no_anomaly():
    service = BehaviourService()

    profile = BehaviourProfile(
        device_id="GX-DRONE-01",
        expected_speed_min=0,
        expected_speed_max=25,
        expected_altitude_min=0,
        expected_altitude_max=120,
        expected_temperature_max=80,
    )

    result = service.analyze(
        profile,
        speed=10,
        altitude=50,
        temperature=40,
    )

    assert result["anomaly_detected"] is False
    assert result["deviation_count"] == 0


def test_abnormal_speed_is_detected():
    service = BehaviourService()

    profile = BehaviourProfile(
        device_id="GX-DRONE-01",
        expected_speed_min=0,
        expected_speed_max=25,
    )

    result = service.analyze(
        profile,
        speed=40,
    )

    assert result["anomaly_detected"] is True
    assert result["deviation_count"] == 1
    assert "Speed above expected range." in result["deviations"]