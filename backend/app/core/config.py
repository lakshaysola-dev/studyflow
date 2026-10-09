from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(ROOT_DIR / ".env", Path(".env")),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "StudyFlow API"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://studyflow:studyflow@localhost:5432/studyflow"

    secret_key: str = "change-me-to-a-long-random-string"
    access_token_expire_minutes: int = 60 * 24 * 7
    jwt_algorithm: str = "HS256"
    credentials_encryption_key: str = ""

    cors_origins: str = "http://localhost:3000"

    llm_provider: str = "gemini"
    gemini_api_key: str = ""
    openai_api_key: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
