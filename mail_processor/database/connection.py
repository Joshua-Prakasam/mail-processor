"""DB Connection."""

import sqlite3
import threading
from pathlib import Path
from typing import Self

from mail_processor.config import app_config

__all__ = ["sqlite_connection"]


class SQLiteConnection:
    """SQLite Connection Singleton."""

    _instance = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        """Initialize the GMail Service."""
        if self._instance is self:
            Path(app_config.SQLITE_DB).parent.mkdir(
                parents=True,
                exist_ok=True,
            )
            self.connection = sqlite3.connect(
                app_config.SQLITE_DB,
            )
            self.cursor = self.connection.cursor()

    def __new__(cls) -> Self:
        """Singleton instance."""
        if not cls._instance:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)

        return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        """Get Connection."""
        return self.connection

    def get_cursor(self) -> sqlite3.Cursor:
        """Get Cursor."""
        return self.cursor

    def commit(self) -> None:
        """Commit to DB."""
        self.connection.commit()

    def close(self) -> None:
        """Close connection."""
        self.connection.close()


sqlite_connection = SQLiteConnection()
