"""Schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

StrPredicateT = Literal[
    "contains",
    "does not contain",
    "equals",
    "does not equal",
]
DatePredicateT = Literal["less than", "greater than"]


class StrCondition(BaseModel):
    """String Condition."""

    field_name: Literal["From", "To", "Subject", "Body"]
    predicate: StrPredicateT
    value: str


class DateCondition(BaseModel):
    """Date Condition."""

    field_name: Literal["Date"]
    predicate: DatePredicateT
    value: int
    unit: Literal["days", "months"]


ActionTypes = Literal[
    "Move Message",
    "Mark as Read",
    "Mark as Unread",
]


class MoveAction(BaseModel):
    """Move Action."""

    type: Literal["Move Message"]
    to: str
    from_: str = Field(alias="from")


class ReadAction(BaseModel):
    """Read Action."""

    type: Literal["Mark as Read"]


class UnreadAction(BaseModel):
    """Unread Action."""

    type: Literal["Mark as Unread"]


ActionsSchema = MoveAction | ReadAction | UnreadAction


class RuleSchema(BaseModel):
    """Rule Schema."""

    name: str
    predicate: Literal["all", "any"]
    conditions: list[StrCondition | DateCondition]
    actions: list[ActionsSchema]
