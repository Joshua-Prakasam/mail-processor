"""Logging Configurations."""

import logging

__all__ = ["logger"]


logger = logging.getLogger("mail_processor")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
