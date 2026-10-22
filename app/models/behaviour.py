from pydantic import BaseModel, Field


class BehaviourProfile(BaseModel):
    device_id: str = Field(min_length=3, max_length=100)

    expected_speed_min: float = 0.0
    expected_speed_max: float = 25.0

    expected_altitude_min: float = 0.0
    expected_altitude_max: float = 120.0

    expected_temperature_max: float = 80.0

    baseline_established: bool = False