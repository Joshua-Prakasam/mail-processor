"""External Services."""

from __future__ import annotations

import base64
import re
from email.utils import parsedate_to_datetime
from typing import Generator, Self, TypedDict

from googleapiclient.discovery import build

from mail_processor.authenticate import get_credentials
from mail_processor.logger import logger
from mail_processor.models.message import Message


class ModifyBody(TypedDict):
    """Modify Body."""

    addLabelIds: list[str]
    removeLabelIds: list[str]


def decode_message(message: dict) -> str | None:
    """Decode Message Object from GMail API."""
    if "parts" in message["payload"]:
        for part in message["payload"]["parts"]:
            if part["mimeType"] == "text/plain":
                encoded_body = part["body"]["data"]
                return base64.urlsafe_b64decode(
                    encoded_body,
                ).decode(
                    "utf-8",
                )
    logger.debug(
        "No plain text message found for "
        f"message_id: {message['id']}",
    )
    return None


email_regex = re.compile(r"<(.*?)>")


def get_email(from_: str) -> str:
    """Parse email."""
    email_match = email_regex.search(from_)
    return email_match.group(1)


class GMailServices:
    """A class to interact with GMail Service."""

    _instance = None

    def __init__(self) -> None:
        """Initialize the GMail Service."""
        if self._instance is self:
            self.credentials = get_credentials()
            self.service = build(
                "gmail",
                "v1",
                credentials=self.credentials,
            )

    def __new__(cls, *args, **kwargs) -> Self:  # noqa: ANN002, ANN003, ARG003
        """Singleton instance."""
        if not cls._instance:
            cls._instance = super().__new__(
                cls,
            )
        return cls._instance

    def get_message_infos(self) -> Generator:
        """Get messages."""
        page_token = None
        while True:
            results = (
                self.service.users()
                .messages()
                .list(userId="me", pageToken=page_token)
                .execute()
            )
            yield results["messages"]
            page_token = results.get("nextPageToken")
            if not page_token:
                break

    def get_message(self, message_id: str) -> Message:
        """Get Message."""
        result = (
            self.service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )
        message = {}
        headers = result["payload"]["headers"]
        key_map = {
            "From": "from",
            "To": "to",
            "Subject": "subject",
            "Date": "date",
        }
        get_value_map = {
            "from": get_email,
            "date": lambda val: parsedate_to_datetime(
                val,
            ).isoformat(),
        }
        for header in headers:
            name = header["name"]
            key = key_map.get(name)
            if key:
                value = get_value_map.get(key, lambda val: val)(
                    header["value"],
                )
                message[key] = value

        return Message(
            message_id=result["id"],
            thread_id=result["threadId"],
            from_=message["from"],
            to=message["to"],
            subject=message["subject"],
            date=message["date"],
            body=decode_message(result),
        )

    def modify_message(
        self,
        message_id: str,
        body: ModifyBody,
    ) -> dict:
        """Add / remove the labels."""
        return (
            self.service.users()
            .messages()
            .modify(userId="me", id=message_id, body=body)
            .execute()
        )

    def get_labels(self) -> list[dict]:
        """Get all the labels."""
        return (
            self.service.users().labels().list(userId="me").execute()
        )
