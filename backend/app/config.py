from __future__ import annotations

import json
import os
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    # ============================================================
    # GEMINI
    # ============================================================

    GEMINI_API_KEY: str = ""

    # Gemini text model.
    GEMINI_TEXT_MODEL: str = "gemini-3.8-flash"

    # Kept for compatibility with the existing project.
    # Image generation will now use Hugging Face.
    GEMINI_IMAGE_MODEL: str = "gemini-3.1-flash-image"

    # ============================================================
    # HUGGING FACE IMAGE GENERATION
    # ============================================================

    HF_TOKEN: str = ""

    # FLUX image model through Hugging Face Inference Providers.
    HF_IMAGE_MODEL: str = "black-forest-labs/FLUX.1-schnell"

    # Automatically select an available provider.
    HF_IMAGE_PROVIDER: str = "auto"

    # ============================================================
    # IMAGE PROVIDER
    # ============================================================

    IMAGE_PROVIDER: str = "huggingface"

    # Allow fallback artwork if the external image API fails.
    ALLOW_IMAGE_FALLBACK: bool = True

    # ============================================================
    # SERVER
    # ============================================================

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # ============================================================
    # DATABASE
    # ============================================================

    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'comiccraft.db'}"

    # ============================================================
    # STORAGE
    # ============================================================

    STORAGE_DIR: str = str(BASE_DIR / "storage")

    # ============================================================
    # CORS
    # ============================================================

    CORS_ORIGINS: list[str] | str = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://comiccraft-ai-iota.vercel.app",
    ]

    @field_validator("CORS_ORIGINS", mode="after")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            value = value.strip()

            if value.startswith("[") and value.endswith("]"):
                try:
                    parsed = json.loads(value)

                    if isinstance(parsed, list):
                        return [
                            str(origin).strip()
                            for origin in parsed
                            if str(origin).strip()
                        ]

                except (
                    json.JSONDecodeError,
                    TypeError,
                    ValueError,
                ):
                    pass

            return [
                origin.strip()
                for origin in value.split(",")
                if origin.strip()
            ]

        return value


settings = Settings()


# ================================================================
# CREATE REQUIRED DIRECTORIES
# ================================================================

os.makedirs(settings.STORAGE_DIR, exist_ok=True)

os.makedirs(
    os.path.join(settings.STORAGE_DIR, "projects"),
    exist_ok=True,
)

os.makedirs(
    os.path.join(settings.STORAGE_DIR, "exports"),
    exist_ok=True,
)

