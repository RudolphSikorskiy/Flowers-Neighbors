from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from telegram_config.data.config import ADMIN_ID
from telegram_config.loader import dp
import logging

log = logging.getLogger(__name__)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    fullname = message.from_user.full_name
    username = message.from_user.username
    telegram_id = message.from_user.id
    await dp.bot.send_message(ADMIN_ID,
                              f"В бота зашел пользователь:\n"
                              f"Telegram ID: <code>{telegram_id}</code>\n"
                              f"Имя: <code>{fullname}</code>\n"
                              f"Username: <code>{username}</code>\n"
                              )

    await message.answer(f'Привет, {message.from_user.full_name}!')
