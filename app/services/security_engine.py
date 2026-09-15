from uuid import uuid4

from app.models.command import Command
from app.models.device import Device
from app.models.enums import SecurityDecision
from app.models.security_event import SecurityEvent
from app.models.user import User
from app.services.event_service import EventService
from app.services.identity_service import IdentityService
from app.services.policy_service import PolicyService
from app.services.risk_service import RiskService


class SecurityEngine:
    """Coordinates GuardianX security evaluation and evidence recording."""

    def __init__(self) -> None:
        self.identity_service = IdentityService()
        self.policy_service = PolicyService()
        self.risk_service = RiskService()
        self.event_service = EventService()

    def _record_evidence(
        self,
        *,
        user: User,
        device: Device,
        command: Command,
        decision: SecurityDecision,
        risk_level: str,
        risk_score: int,
        reason: str,
    ) -> None:
        event_id = str(uuid4())

        event = SecurityEvent(
            event_id=event_id,
            device_id=device.device_id,
            event_type="COMMAND_EVALUATION",
            source="security-engine",
            risk_level=risk_level,
            decision=decision,
            message=reason,
            details={
                "command_id": command.command_id,
                "command_type": command.command_type,
                "user_id": user.user_id,
                "risk_score": risk_score,
            },
        )

        self.event_service.record_security_event(event)

        self.event_service.record_audit_log(
            actor_id=user.user_id,
            action="COMMAND_EVALUATED",
            resource_type="DEVICE",
            resource_id=device.device_id,
            outcome=decision.value,
            event_id=event_id,
            details={
                "command_id": command.command_id,
                "command_type": command.command_type,
                "risk_level": risk_level,
                "risk_score": risk_score,
                "reason": reason,
            },
        )

    def evaluate(
        self,
        *,
        user: User,
        device: Device,
        command: Command,
    ) -> dict:
        if not self.identity_service.verify_user(user):
            decision = SecurityDecision.BLOCK
            risk_level = "HIGH"
            risk_score = 50
            reason = "User identity is inactive."

        elif not self.identity_service.verify_device(device):
            decision = SecurityDecision.BLOCK
            risk_level = "HIGH"
            risk_score = 50
            reason = "Device is inactive or untrusted."

        elif device.owner_id != user.user_id:
            decision = SecurityDecision.BLOCK
            risk_level = "HIGH"
            risk_score = 50
            reason = "User is not the owner of the device."

        elif command.device_id != device.device_id:
            decision = SecurityDecision.BLOCK
            risk_level = "HIGH"
            risk_score = 50
            reason = "Command targets a different device."

        elif command.issued_by != user.user_id:
            decision = SecurityDecision.BLOCK
            risk_level = "HIGH"
            risk_score = 50
            reason = "Command issuer does not match the authenticated user."

        else:
            policy_decision = self.policy_service.evaluate(user, command)

            if policy_decision == SecurityDecision.BLOCK:
                decision = SecurityDecision.BLOCK
                risk_level_enum, risk_score = self.risk_service.calculate(
                    denied=True
                )
                risk_level = risk_level_enum.value
                reason = "Command blocked by security policy."
            else:
                decision = SecurityDecision.ALLOW
                risk_level_enum, risk_score = self.risk_service.calculate()
                risk_level = risk_level_enum.value
                reason = (
                    "Command passed identity, ownership, trust, and policy checks."
                )

        self._record_evidence(
            user=user,
            device=device,
            command=command,
            decision=decision,
            risk_level=risk_level,
            risk_score=risk_score,
            reason=reason,
        )

        return {
            "decision": decision,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "reason": reason,
        }