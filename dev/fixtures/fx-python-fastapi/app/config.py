"""Application configuration via Pydantic v2 Settings.

Trampa E04: las settings cambian segun el entorno (DATABASE_URL,
TESTING flag). La skill debe leer este archivo para entender como
cambia el comportamiento entre dev/prod.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "sqlite+aiosqlite:///./fxfast.db"
    TESTING: bool = False
    SECRET_KEY: str = "fxfast-insecure-secret-key-only-for-dev"
    API_TITLE: str = "fxfast"
    API_VERSION: str = "1.0.0"


settings = Settings()