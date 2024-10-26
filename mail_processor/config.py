"""APP Level Settings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["app_config"]


class Settings(BaseSettings):
    """App level setting."""

    CREDENTIALS_JSON_PATH: Path
    TOKEN_JSON_PATH: Path

    SQLITE_DB: Path

    model_config = SettingsConfigDict(env_file=".env")


app_config = Settings()
