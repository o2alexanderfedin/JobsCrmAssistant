"""Configuration management for the application."""
from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CorsSettings(BaseSettings):
    """Settings the API needs at startup, none of them required."""

    # Origins allowed to call the API from a browser, as a JSON list in
    # CORS_ORIGINS, e.g. CORS_ORIGINS='["http://localhost:3000"]'.
    cors_origins: List[str] = Field(
        default_factory=list, description="Allowed CORS origins"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # .env also holds the settings below; they are not errors here.
        extra="ignore",
    )


class Settings(CorsSettings):
    """Application settings."""

    # API Configuration
    api_prefix: str = "/api/v1"
    debug: bool = False

    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")
    openai_model: str = Field("gpt-4", description="OpenAI model to use")

    # Database Configuration
    database_url: Optional[str] = None

    model_config = SettingsConfigDict(extra="forbid")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
