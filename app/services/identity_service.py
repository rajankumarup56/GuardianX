from app.models.device import Device
from app.models.user import User


class IdentityService:
    """Handles basic identity and trust checks."""

    def verify_user(self, user: User) -> bool:
        return user.active

    def verify_device(self, device: Device) -> bool:
        return device.active and device.trusted