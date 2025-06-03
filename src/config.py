# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    ENV_NAME: str = "local"
    AWS_REGION: str = "eu-west-3"  # Corrigé depuis AWS_REGION_NAME
    DYNAMO_TABLE: str = ""
    AWS_PROFILE: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    MISTRAL_API_KEY: str = ""
    
    # Configuration Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_WEBHOOK_URL: str = ""
    TELEGRAM_WEBHOOK_PATH: str = "/telegram/webhook"
    
    # Configuration API
    API_URL: str = "http://localhost:8001"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


@lru_cache
def get_settings():
    return settings


env_vars = get_settings()
