import json
from datetime import datetime, timezone
from typing import Any

from app.db.database import get_connection
from app.models.security_event import SecurityEvent


class EventService:
    """Persists and retrieves GuardianX security events and audit records."""

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

    def list_security_events(self, limit: int = 50) -> list[dict[str, Any]]:
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    event_id,
                    device_id,
                    event_type,
                    source,
                    risk_level,
                    decision,
                    message,
                    details,
                    created_at
                FROM security_events
                ORDER BY rowid DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

            return [
                {
                    "event_id": row["event_id"],
                    "device_id": row["device_id"],
                    "event_type": row["event_type"],
                    "source": row["source"],
                    "risk_level": row["risk_level"],
                    "decision": row["decision"],
                    "message": row["message"],
                    "details": json.loads(row["details"]),
                    "created_at": row["created_at"],
                }
                for row in rows
            ]
        finally:
            connection.close()

    def list_audit_logs(self, limit: int = 50) -> list[dict[str, Any]]:
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    audit_id,
                    event_id,
                    actor_id,
                    action,
                    resource_type,
                    resource_id,
                    outcome,
                    details,
                    created_at
                FROM audit_logs
                ORDER BY audit_id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

            return [
                {
                    "audit_id": row["audit_id"],
                    "event_id": row["event_id"],
                    "actor_id": row["actor_id"],
                    "action": row["action"],
                    "resource_type": row["resource_type"],
                    "resource_id": row["resource_id"],
                    "outcome": row["outcome"],
                    "details": json.loads(row["details"]),
                    "created_at": row["created_at"],
                }
                for row in rows
            ]
        finally:
            connection.close()