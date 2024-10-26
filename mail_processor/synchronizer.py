"""Synchronize local DB with Gmail Mails."""

from rich.progress import Progress

from mail_processor.logger import logger
from mail_processor.models.message import Message
from mail_processor.models.message_info import MessageInfo
from mail_processor.services import GMailServices

__all__ = ["sync_emails"]


def sync_emails(*, refresh: bool = False) -> None:
    """Synchronize the mails."""
    service = GMailServices()

    for message_infos in service.get_message_infos():
        message_objects = [
            MessageInfo(
                message_id=message_info["id"],
                thread_id=message_info["threadId"],
            )
            for message_info in message_infos
        ]

        MessageInfo.bulk_insert(message_objects)

    if refresh:
        Message.delete_all()
        message_infos = MessageInfo.get_all()
    else:
        message_ids = [
            message.message_id for message in Message.get_all()
        ]

        message_infos = (
            MessageInfo.get_message_infos_by_ids(
                message_ids,
            )
            if message_ids
            else MessageInfo.get_all()
        )

    if not message_infos:
        logger.info("Already synced with mail.")
        return

    with Progress() as progress:
        task = progress.add_task(
            "Syncing...",
            total=len(message_infos),
        )
        for message_info_obj in message_infos:
            service.get_message(message_info_obj.message_id).save()
            progress.update(task, advance=1)
