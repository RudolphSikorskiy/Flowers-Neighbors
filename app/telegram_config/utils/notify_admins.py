import logging

from aiogram import Dispatcher

from telegram_config.data.config import ADMIN_ID


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(ADMIN_ID, "Бот Запущен")

    except Exception as err:
        logging.exception(err)
