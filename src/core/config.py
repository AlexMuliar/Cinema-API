import os

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.logger import get_logger

logger = get_logger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    SECRET_KEY: str = os.environ.get("AUTH_SECRET_KEY")
    REFRESH_SECRET_KEY: str = os.environ.get("AUTH_REFRESH_SECRET_KEY")
    ALGORITHM: str = os.environ.get("AUTH_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get(
        "AUTH_ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = os.environ.get(
        "AUTH_REFRESH_TOKEN_EXPIRE_MINUTES", 1440)
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER", "postgres-db")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB", "postgres")
    POSTGRES_PORT: int = os.environ.get("POSTGRES_PORT", 5432)
    POSTGRES_URL: str = f"postgresql://{POSTGRES_USER}:{
        POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()
