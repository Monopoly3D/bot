from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config import Config

config = Config(_env_file=".env")

bot = Bot(
    token=config.telegram_bot_token.get_secret_value(),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)


def create_dispatcher() -> Dispatcher:
    storage: RedisStorage | None = None

    if config.redis_dsn is not None:
        redis = Redis.from_url(config.redis_dsn.get_secret_value())
        storage = RedisStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True))

    new_dispatcher = Dispatcher(storage=storage)

    new_dispatcher.workflow_data.update(
        {
            "config": config
        }
    )

    return new_dispatcher


async def main() -> None:
    dispatcher = create_dispatcher()

    await dispatcher.start_polling(bot)
