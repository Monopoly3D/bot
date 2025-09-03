from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    telegram_bot_token: SecretStr
    redis_dsn: SecretStr | None = None
