"""Central application configuration loaded from environment variables."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated configuration shared across the FastAPI application."""

    # Application identity and runtime environment.
    APP_NAME: str = "Sikh Anandkaraj API"
    APP_ENV: Literal["development", "testing", "qa", "production"] = "development"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # PostgreSQL connection URL.
    DATABASE_URL: str

    # Redis connection URL.
    REDIS_URL: str

    # Frontend origins permitted to call the API.
    ALLOWED_ORIGINS: list[str] = Field(default_factory=list)

    # Authentication configuration.
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Avoid accidental acceptance of undeclared environment variables.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def is_production(self) -> bool:
        """Return whether the API is running in production."""

        return self.APP_ENV == "production"


@lru_cache
def get_settings() -> Settings:
    """Create one cached and validated settings instance."""

    return Settings()