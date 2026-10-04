import os
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    # Gemini configuration
    GEMINI_API_KEY: str = ""
    GEMINI_TEXT_MODEL: str = "gemini-2.5-flash"
    GEMINI_IMAGE_MODEL: str = "imagen-3.0-generate-002"

    # Server configuration
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'comiccraft.db'}"

    # Storage
    STORAGE_DIR: str = str(BASE_DIR / "storage")

    # CORS
    CORS_ORIGINS: list[str] | str = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://comiccraft-ai-iota.vercel.app",
    ]

    # Image provider
    IMAGE_PROVIDER: str = "gemini"

    @field_validator("CORS_ORIGINS", mode="after")
    @classmethod
    def parse_cors_origins(cls, value):
        """
        Convert CORS_ORIGINS from an environment-variable string
        into a list of allowed origins.
        """

        if isinstance(value, str):
            value = value.strip()

            # Support JSON-style lists:
            # ["http://localhost:5173", "https://example.com"]
            if value.startswith("[") and value.endswith("]"):
                import json

                try:
                    parsed = json.loads(value)

                    if isinstance(parsed, list):
                        return [
                            str(origin).strip()
                            for origin in parsed
                            if str(origin).strip()
                        ]
                except (json.JSONDecodeError, TypeError, ValueError):
                    pass

            # Support comma-separated values:
            # http://localhost:5173,https://example.com
            return [
                origin.strip()
                for origin in value.split(",")
                if origin.strip()
            ]

        return value


# Create application settings
settings = Settings()


# Ensure storage directories exist
os.makedirs(settings.STORAGE_DIR, exist_ok=True)

os.makedirs(
    os.path.join(settings.STORAGE_DIR, "projects"),
    exist_ok=True
)

os.makedirs(
    os.path.join(settings.STORAGE_DIR, "exports"),
    exist_ok=True
)