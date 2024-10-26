"""Rule Engine which parses and executes rules."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from pydantic import ValidationError

from mail_processor.logger import logger
from mail_processor.models.message import Message
from mail_processor.rule_engine.schema import (
    ActionsSchema,
    ActionTypes,
    DateCondition,
    MoveAction,
    ReadAction,
    RuleSchema,
    StrCondition,
    UnreadAction,
)
from mail_processor.services import GMailServices, ModifyBody

__all__ = ["execute_rules"]


def get_clause(condition: DateCondition | StrCondition) -> str:
    field_name = condition.field_name.lower()
    if isinstance(condition, DateCondition):
        operator = "<"
        if condition.predicate == "less than":
            operator = ">"
        value = f"DATE('now', '-{condition.value} {condition.unit}')"
    else:
        operator = "="
        if condition.predicate == "contains":
            operator = "LIKE"
        elif condition.predicate == "does not contain":
            operator = "NOT LIKE"
        elif condition.predicate == "does not equal":
            operator = "!="

        # NOTE: To be in-case sensitive search in text column
        field_name = f'LOWER("{field_name}")'
        value = f"LOWER('{condition.value}')"

    return f"{field_name} {operator} {value}"


def filter_messages(rule_obj: RuleSchema) -> list[Message]:
    join_str = " OR "
    if rule_obj.predicate == "all":
        join_str = " AND "

    where_clause = join_str.join(
        get_clause(condition) for condition in rule_obj.conditions
    )

    return Message.get_by_filter(where_clause=where_clause)


class ActionExecutor:
    def __init__(
        self,
        rule_obj: RuleSchema,
        filtered_messages: list[Message],
    ) -> None:
        """Initialize Action Executor."""
        self.rule_obj = rule_obj
        self.filtered_message = filtered_messages
        self.service = GMailServices()
        self.action_map: dict[ActionTypes, Callable] = {
            "Mark as Read": self.__mark_as_read,
            "Mark as Unread": self.__mark_as_unread,
            "Move Message": self.__move_message,
        }

    def __mark_as_read(self, __action: ReadAction) -> None:
        """Mark messages as Read."""
        body: ModifyBody = {
            "addLabelIds": [],
            "removeLabelIds": ["UNREAD"],
        }
        for message in self.filtered_message:
            self.service.modify_message(
                message_id=message.message_id,
                body=body,
            )

    def __mark_as_unread(self, __action: UnreadAction) -> None:
        """Mark messages as Unread."""
        body: ModifyBody = {
            "addLabelIds": ["UNREAD"],
            "removeLabelIds": [],
        }
        for message in self.filtered_message:
            self.service.modify_message(
                message_id=message.message_id,
                body=body,
            )

    def __move_message(self, __action: MoveAction) -> None:
        body: ModifyBody = {
            "addLabelIds": [__action.to],
            "removeLabelIds": [__action.from_],
        }
        for message in self.filtered_message:
            result = self.service.modify_message(
                message_id=message.message_id,
                body=body,
            )
            logger.info(f"Move Result: {result}")

    def __run_action(self, action: ActionsSchema) -> None:
        """Run a single action."""
        self.action_map[action.type](action)

    def execute(self) -> None:
        """Execute all the actions."""
        for action in self.rule_obj.actions:
            self.__run_action(action)
            logger.info(
                f"Processed {len(self.filtered_message)} messages "
                f"for rule: {self.rule_obj.name}",
            )


def get_rule_obj(rule: dict) -> None | RuleSchema:
    """Get RuleSchema object."""
    try:
        return RuleSchema(**rule)
    except ValidationError as e:
        logger.error(e)


def execute_rules(file_path: str) -> None:
    """Entry point for rule execution."""
    with Path(file_path).open() as fp:
        rules = json.load(fp)

    for i, rule in enumerate(rules):
        rule_obj = get_rule_obj(rule)
        if not rule_obj:
            logger.warning(f"Skipping item in {i+1}")
            continue

        logger.info(f"Processing rule: {rule_obj.name}")

        filtered_messages = filter_messages(rule_obj)
        action_executor = ActionExecutor(
            rule_obj=rule_obj,
            filtered_messages=filtered_messages,
        )

        action_executor.execute()
