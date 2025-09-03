from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart

from app.scenes.start import StartScene

start_router = Router(name=__name__)

start_router.message.register(
    StartScene.as_handler(),
    CommandStart(),
    F.chat.type == ChatType.PRIVATE
)
