from app.models.command import Command
from app.models.device import Device
from app.models.enums import SecurityDecision
from app.models.user import User
from app.services.identity_service import IdentityService
from app.services.policy_service import PolicyService
from app.services.risk_service import RiskService


class SecurityEngine:
    """Coordinates GuardianX identity, ownership, policy, and risk evaluation."""

    def __init__(self) -> None:
        self.identity_service = IdentityService()
        self.policy_service = PolicyService()
        self.risk_service = RiskService()

    def evaluate(
        self,
        *,
        user: User,
        device: Device,
        command: Command,
    ) -> dict:
        if not self.identity_service.verify_user(user):
            return {
                "decision": SecurityDecision.BLOCK,
                "risk_level": "HIGH",
                "risk_score": 50,
                "reason": "User identity is inactive.",
            }

        if not self.identity_service.verify_device(device):
            return {
                "decision": SecurityDecision.BLOCK,
                "risk_level": "HIGH",
                "risk_score": 50,
                "reason": "Device is inactive or untrusted.",
            }

        if device.owner_id != user.user_id:
            return {
                "decision": SecurityDecision.BLOCK,
                "risk_level": "HIGH",
                "risk_score": 50,
                "reason": "User is not the owner of the device.",
            }

        if command.device_id != device.device_id:
            return {
                "decision": SecurityDecision.BLOCK,
                "risk_level": "HIGH",
                "risk_score": 50,
                "reason": "Command targets a different device.",
            }

        if command.issued_by != user.user_id:
            return {
                "decision": SecurityDecision.BLOCK,
                "risk_level": "HIGH",
                "risk_score": 50,
                "reason": "Command issuer does not match the authenticated user.",
            }

        policy_decision = self.policy_service.evaluate(user, command)

        if policy_decision == SecurityDecision.BLOCK:
            risk_level, risk_score = self.risk_service.calculate(denied=True)

            return {
                "decision": SecurityDecision.BLOCK,
                "risk_level": risk_level.value,
                "risk_score": risk_score,
                "reason": "Command blocked by security policy.",
            }

        risk_level, risk_score = self.risk_service.calculate()

        return {
            "decision": SecurityDecision.ALLOW,
            "risk_level": risk_level.value,
            "risk_score": risk_score,
            "reason": "Command passed identity, ownership, trust, and policy checks.",
        }