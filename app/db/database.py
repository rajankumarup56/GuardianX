import sqlite3

from app.core.config import settings


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(
        settings.database_url.replace("sqlite:///", ""),
        check_same_thread=False,
    )
    connection.row_factory = sqlite3.Row
    return connection