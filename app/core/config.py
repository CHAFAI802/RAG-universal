import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", "5433"))
    DB_NAME: str = os.getenv("DB_NAME", "")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    AUTH_TOKEN_SECRET: str = os.getenv("AUTH_TOKEN_SECRET", "")
    AUTH_TOKEN_TTL_SECONDS: int = int(os.getenv("AUTH_TOKEN_TTL_SECONDS", "900"))


settings = Settings()
