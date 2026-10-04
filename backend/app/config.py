import os
from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    GEMINI_API_KEY: str = ""
    GEMINI_TEXT_MODEL: str = "gemini-2.5-flash"
    GEMINI_IMAGE_MODEL: str = "imagen-3.0-generate-002"
    
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'comiccraft.db'}"
    STORAGE_DIR: str = str(BASE_DIR / "storage")
    CORS_ORIGINS: list[str] | str = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    IMAGE_PROVIDER: str = "gemini"

    @field_validator("CORS_ORIGINS", mode="after")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

settings = Settings()

# Ensure storage subdirectories exist
os.makedirs(settings.STORAGE_DIR, exist_ok=True)
os.makedirs(os.path.join(settings.STORAGE_DIR, "projects"), exist_ok=True)
os.makedirs(os.path.join(settings.STORAGE_DIR, "exports"), exist_ok=True)
