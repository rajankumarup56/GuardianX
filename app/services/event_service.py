import json
from datetime import datetime, timezone
from typing import Any

from app.db.database import get_connection
from app.models.security_event import SecurityEvent


class EventService:
    """Persists GuardianX security events and audit records in SQLite."""

    def record_security_event(self, event: SecurityEvent) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO security_events (
                    event_id,
                    device_id,
                    event_type,
                    source,
                    risk_level,
                    decision,
                    message,
                    details,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.device_id,
                    event.event_type,
                    event.source,
                    event.risk_level.value,
                    event.decision.value,
                    event.message,
                    json.dumps(event.details),
                    event.created_at.isoformat(),
                ),
            )

            connection.commit()
        finally:
            connection.close()

    def record_audit_log(
        self,
        *,
        actor_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        outcome: str,
        event_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO audit_logs (
                    event_id,
                    actor_id,
                    action,
                    resource_type,
                    resource_id,
                    outcome,
                    details,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    actor_id,
                    action,
                    resource_type,
                    resource_id,
                    outcome,
                    json.dumps(details or {}),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )

            connection.commit()
        finally:
            connection.close()