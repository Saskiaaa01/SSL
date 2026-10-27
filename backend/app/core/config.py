import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SSLGuard — SSL Certificate Monitoring & WhatsApp Alert System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Security & JWT
    SECRET_KEY: str = "sslguard-kominfo-pkl2026-super-secret-key-32bytes-min"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 hari

    # Database: Default SQLite for zero-config local run, supports PostgreSQL
    DATABASE_URL: str = "sqlite:///./sslguard.db"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5500",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:8000",
        "*",
    ]

    # SSL Inspection Settings
    SSL_DEFAULT_PORT: int = 443
    SSL_SOCKET_TIMEOUT_SECONDS: int = 5
    SSRF_PROTECTION_ENABLED: bool = True

    # Scheduler Settings
    SCHEDULER_ENABLED: bool = True
    SCHEDULER_CRON_HOUR: int = 7
    SCHEDULER_CRON_MINUTE: int = 0
    TIMEZONE: str = "Asia/Jakarta"

    # WhatsApp Cloud API / Webhook Settings
    WHATSAPP_SIMULATION_MODE: bool = True
    WHATSAPP_API_URL: str = "https://graph.facebook.com/v19.0"
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    WHATSAPP_ACCESS_TOKEN: str = ""
    WHATSAPP_ADMIN_PHONE: str = "+6281198765432"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
