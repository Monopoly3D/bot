from aiogram.fsm.scene import on
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, User
from aiogram.utils.i18n import gettext as _

from app.scenes.abstract import AbstractScene


class StartScene(AbstractScene, state="start", reset_history_on_enter=True):
    __STARTAPP_URL = "https://t.me/{bot_username}/?startapp"

    @on.message.enter()
    async def on_start_command(
            self,
            message: Message
    ) -> None:
        bot_user: User = await message.bot.get_me()

        reply_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=_("button.enter_game"),
                        url=self.__STARTAPP_URL.format(bot_username=bot_user.username)
                    )
                ]
            ]
        )

        await message.answer(
            _("start.private"),
            reply_markup=reply_markup
        ),

        await message.delete()

    @on.message()
    async def on_message(
            self,
            message: Message
    ) -> None:
        await message.delete()
