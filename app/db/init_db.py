from app.db.database import get_connection


def init_db() -> None:
    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS security_events (
                event_id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                source TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                decision TEXT NOT NULL,
                message TEXT NOT NULL,
                details TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_logs (
                audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT,
                actor_id TEXT NOT NULL,
                action TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                resource_id TEXT NOT NULL,
                outcome TEXT NOT NULL,
                details TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL
            )
            """
        )

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    init_db()
    print("GuardianX database initialized successfully.")