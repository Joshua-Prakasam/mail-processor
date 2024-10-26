"""Authenticate GMail."""

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from mail_processor.config import app_config
from mail_processor.constants import (
    SCOPES,
)
from mail_processor.errors import NoAuthenticationError
from mail_processor.logger import logger


def store_credentials() -> None:
    """Store Credentials."""
    # If there are no (valid) credentials available,
    # let the user log in.
    if Path(app_config.TOKEN_JSON_PATH).exists():
        logger.info("Already authenticated.")
        return

    flow = InstalledAppFlow.from_client_secrets_file(
        app_config.CREDENTIALS_JSON_PATH,
        SCOPES,
    )
    flow.run_local_server(port=0)

    with Path.open(app_config.TOKEN_JSON_PATH, "w") as token:
        token.write(Credentials.to_json())


def get_credentials() -> Credentials:
    """Get authenticated credentials.

    :raises NoAuthenticationError: If no token found.
    :return: an instance of Credentials
    """
    if not Path(app_config.TOKEN_JSON_PATH).exists():
        raise NoAuthenticationError

    credentials: Credentials = Credentials.from_authorized_user_file(
        app_config.TOKEN_JSON_PATH,
        SCOPES,
    )

    if (
        credentials
        and credentials.expired
        and credentials.refresh_token
    ):
        credentials.refresh(Request())

    return credentials
