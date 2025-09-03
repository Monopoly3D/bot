from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n, FSMI18nMiddleware
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from aiohttp.web import Application
from redis.asyncio import Redis

from app.routes.start import start_router
from app.scenes.start import StartScene
from config import Config

config = Config(_env_file=".env")


def create_dispatcher() -> Dispatcher:
    storage: RedisStorage | None = None

    if config.redis_dsn is not None:
        redis = Redis.from_url(config.redis_dsn.get_secret_value())
        storage = RedisStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True))

    new_dispatcher = Dispatcher(storage=storage)

    i18n = I18n(path="locales", default_locale="en", domain="messages")

    new_dispatcher.workflow_data.update(
        {
            "config": config,
            "i18n": i18n
        }
    )

    FSMI18nMiddleware(i18n).setup(new_dispatcher)

    new_dispatcher.include_routers(
        start_router
    )

    registry = SceneRegistry(new_dispatcher)
    registry.add(
        StartScene
    )

    return new_dispatcher


async def on_startup(bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)

    await bot.set_webhook(
        config.webhook_url.get_secret_value(),
        secret_token=config.telegram_secret.get_secret_value()
    )


async def main_polling() -> None:
    dispatcher = create_dispatcher()

    bot = Bot(
        token=config.telegram_bot_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    await dispatcher.start_polling(bot)


def main_webhook() -> None:
    dispatcher = create_dispatcher()
    dispatcher.startup.register(on_startup)

    bot = Bot(
        token=config.telegram_bot_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    app = Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=config.telegram_secret.get_secret_value(),
    )
    webhook_requests_handler.register(app, path=config.webhook_path.get_secret_value())

    setup_application(app, dispatcher, bot=bot)

    web.run_app(
        app,
        host="0.0.0.0",
        port=8080
    )
