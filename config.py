from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    telegram_bot_token: SecretStr
    telegram_secret: SecretStr
    webhook_url: SecretStr
    webhook_path: SecretStr
    redis_dsn: SecretStr | None = None
