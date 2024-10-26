"""Application Errors."""

from __future__ import annotations

from typing import Any


class NoAuthenticationError(Exception):
    """No Authentication Error."""

    def __init__(self, *args: tuple[Any, ...]) -> None:
        """Initialise with default message."""
        message = "No token found."
        super().__init__(message, *args)


class UnInitializedError(Exception):
    """Un Initialized Error."""

    def __init__(self, *args: tuple[Any, ...]) -> None:
        """Initialize with default message."""
        message = "Instance not initialized."
        super().__init__(message, *args)
