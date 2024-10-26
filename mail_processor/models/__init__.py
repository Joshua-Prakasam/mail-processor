"""Module entry for models."""

from mail_processor.models.message import Message
from mail_processor.models.message_info import MessageInfo


def initialize_models() -> None:
    """Initialize Models in DB."""
    models = [MessageInfo, Message]
    for model in models:
        model.create_table()
