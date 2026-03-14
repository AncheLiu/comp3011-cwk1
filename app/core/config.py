from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Deadlock Meta Intelligence API"
    app_version: str = "0.1.0"
    database_url: str = Field(
        default=f"sqlite:///{(PROJECT_ROOT / 'deadlock_meta.db').as_posix()}",
        description="Database connection string for local development or deployment.",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
