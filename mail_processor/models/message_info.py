"""Message Info Model."""

from __future__ import annotations

from mail_processor.database.connection import sqlite_connection

conn = sqlite_connection.get_connection()


class MessageInfo:
    """Model for message_info table."""

    table_name = "message_info"

    def __init__(self, message_id: str, thread_id: str) -> None:
        """Initialize Message Info attribute."""
        self.message_id = message_id
        self.thread_id = thread_id

    @staticmethod
    def create_table() -> None:
        """Create table."""
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {MessageInfo.table_name} (
                message_id TEXT PRIMARY KEY,
                thread_id TEXT NOT NULL
            )
        """)
        conn.commit()

    @staticmethod
    def bulk_insert(message_infos: list[MessageInfo]) -> None:
        """Store multiple message_infos."""
        cursor = conn.cursor()
        message_info_values = [
            (message_info.message_id, message_info.thread_id)
            for message_info in message_infos
        ]
        cursor.executemany(
            f"""
                INSERT OR IGNORE INTO {MessageInfo.table_name}
                    (message_id, thread_id)
                VALUES (?, ?)
            """,
            message_info_values,
        )
        conn.commit()

    def save(self) -> None:
        """Save the entry."""
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO {self.table_name}
                (message_id, thread_id)
            VALUES
                (?, ?)
            """,
            (self.message_id, self.thread_id),
        )
        conn.commit()

    @staticmethod
    def get_all() -> list[MessageInfo]:
        """Get All MessageInfo's."""
        cursor = conn.cursor()
        cursor.execute(
            "SELECT message_id, thread_id "
            f"FROM {MessageInfo.table_name}",
        )
        return [
            MessageInfo(
                message_id=message_info[0],
                thread_id=message_info[1],
            )
            for message_info in cursor.fetchall()
        ]

    @staticmethod
    def get_by_message_id(message_id: str) -> MessageInfo | None:
        """Get By Message Id."""
        cursor = conn.cursor()
        cursor.execute(
            f"""
                SELECT message_id, thread_id
                FROM {MessageInfo.table_name} WHERE message_id = ?
            """,
            (message_id,),
        )
        message_info = cursor.fetchone()
        if message_info:
            return MessageInfo(
                message_id=message_info[0],
                thread_id=message_info[1],
            )
        return None

    @staticmethod
    def delete(message_id: str) -> None:
        """Delete message info by message_id."""
        cursor = conn.cursor()
        cursor.execute(
            f"DELETE FROM {MessageInfo.table_name} WHERE id = ?",
            (message_id,),
        )
        conn.commit()

    @staticmethod
    def get_message_infos_by_ids(message_ids: list[str]):
        cursor = conn.cursor()
        placeholders = ", ".join("?" for _ in message_ids)
        cursor.execute(
            f"""
                SELECT message_id, thread_id
                FROM {MessageInfo.table_name}
                WHERE message_id NOT IN ({placeholders})
            """,
            message_ids,
        )
        return [
            MessageInfo(
                message_id=message_info[0],
                thread_id=message_info[1],
            )
            for message_info in cursor.fetchall()
        ]
