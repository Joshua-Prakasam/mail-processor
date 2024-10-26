#!/usr/bin/env python

"""Entrypoint for the cli application."""

from mail_processor.authenticate import (
    store_credentials,
)
from mail_processor.cli import get_parser
from mail_processor.logger import logger
from mail_processor.models import initialize_models
from mail_processor.rule_engine import execute_rules
from mail_processor.services import GMailServices
from mail_processor.synchronizer import sync_emails


def main() -> None:
    """Entry point to app."""
    initialize_models()

    parser = get_parser()
    args = parser.parse_args()

    if args.subcommand == "auth":
        store_credentials()
    elif args.subcommand == "sync":
        sync_emails(refresh=args.refresh)
    elif args.subcommand == "labels":
        logger.info(GMailServices().get_labels())
    elif args.subcommand == "execute":
        execute_rules(args.file_path)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
