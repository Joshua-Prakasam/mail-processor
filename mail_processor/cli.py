"""CLI for the app."""

from argparse import ArgumentParser


def get_parser() -> ArgumentParser:
    """Get Configured Parser."""
    parser: ArgumentParser = ArgumentParser(
        prog="mail_processor",
        description=(
            "Synchronizes with gmail and do actions "
            "based on the rules configured."
        ),
    )

    subparsers = parser.add_subparsers(
        dest="subcommand",
        required=True,
    )
    subparsers.add_parser(
        "auth",
        description="Authenticates the user with gmail",
    )
    sync_parser = subparsers.add_parser(
        "sync",
        description=(
            "Synchronizes email messages with the application"
        ),
    )
    sync_parser.add_argument(
        "-r",
        "--refresh",
        action="store_true",
        dest="refresh",
        help="Clear all the old message and sync.",
    )
    subparsers.add_parser(
        "labels",
        description="List all the labels",
    )
    execute_parser = subparsers.add_parser(
        "execute",
        description="Execute the given rule",
    )

    execute_parser.add_argument(
        "file_path",
        help="Relative or absolute path to the rules json.",
    )

    return parser
