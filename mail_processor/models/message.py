"""Message Info Model."""

from __future__ import annotations

from mail_processor.database.connection import sqlite_connection

conn = sqlite_connection.get_connection()


class Message:
    """Model for message table."""

    table_name = "message"

    def __init__(  # noqa: PLR0913
        self,
        message_id: str,
        thread_id: str,
        from_: str,
        to: str,
        subject: str,
        date: str,
        body: str,
    ) -> None:
        """Initialize Message Info attribute."""
        self.message_id = message_id
        self.thread_id = thread_id
        self.from_ = from_
        self.to = to
        self.subject = subject
        self.date = date
        self.body = body

    @staticmethod
    def create_table() -> None:
        """Create table."""
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {Message.table_name} (
                message_id TEXT PRIMARY KEY,
                thread_id TEXT,
                "from" TEXT,
                "to" TEXT,
                subject TEXT,
                date TEXT,
                body TEXT
            )
        """)
        conn.commit()

    @staticmethod
    def bulk_insert(messages: list[Message]) -> None:
        """Store multiple message."""
        cursor = conn.cursor()
        message_info_values = [
            (
                message.message_id,
                message.thread_id,
                message.from_,
                message.to,
                message.subject,
                message.date,
                message.body,
            )
            for message in messages
        ]
        cursor.executemany(
            f"""
                INSERT OR IGNORE INTO {Message.table_name}
                    (message_id, thread_id, "from", "to", subject, date, body)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            message_info_values,
        )
        conn.commit()

    def save(self) -> None:
        """Save the entry."""
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT OR IGNORE INTO {Message.table_name}
                    (message_id, thread_id, "from", "to", subject, date, body)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                self.message_id,
                self.thread_id,
                self.from_,
                self.to,
                self.subject,
                self.date,
                self.body,
            ),
        )
        conn.commit()

    @staticmethod
    def get_all() -> list[Message]:
        """Get All Message's."""
        cursor = conn.cursor()
        cursor.execute(
            "SELECT "
            'message_id, thread_id, "from", "to", subject, date, body '
            f"FROM {Message.table_name}",
        )
        return [
            Message(
                message_id=message[0],
                thread_id=message[1],
                from_=message[2],
                to=message[3],
                subject=message[4],
                date=message[5],
                body=message[6],
            )
            for message in cursor.fetchall()
        ]

    @staticmethod
    def get_by_message_id(message_id: str) -> Message | None:
        """Get By Message Id."""
        cursor = conn.cursor()
        cursor.execute(
            "SELECT "
            'message_id, thread_id, "from", "to", subject, date, body '
            f"FROM {Message.table_name} WHERE id = ?",
            (message_id,),
        )
        message = cursor.fetchone()
        if message:
            return Message(
                message_id=message[0],
                thread_id=message[1],
                from_=message[2],
                to=message[3],
                subject=message[4],
                date=message[5],
                body=message[6],
            )
        return None

    @staticmethod
    def get_by_filter(where_clause: str) -> list[Message]:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT "
            'message_id, thread_id, "from", "to", subject, date, body '
            f"FROM {Message.table_name} "
            f"WHERE {where_clause}",
        )
        return [
            Message(
                message_id=message[0],
                thread_id=message[1],
                from_=message[2],
                to=message[3],
                subject=message[4],
                date=message[5],
                body=message[6],
            )
            for message in cursor.fetchall()
        ]

    @staticmethod
    def delete(message_id: str) -> None:
        """Delete message by message_id."""
        cursor = conn.cursor()
        cursor.execute(
            f"DELETE FROM {Message.table_name} WHERE id = ?",
            (message_id,),
        )
        conn.commit()

    @staticmethod
    def delete_all() -> None:
        """Delete all messages."""
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {Message.table_name}")
        conn.commit()
