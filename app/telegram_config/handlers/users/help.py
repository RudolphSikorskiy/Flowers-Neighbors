from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from telegram_config.loader import dp
from telegram_config.utils.misc import rate_limit

import logging

from django_project.settings import MEDIA_ROOT

log = logging.getLogger(__name__)


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/order - Создать заказ',
        '/reset - Перезагрузить бота',
        '/help - Получить справку'
    ]
    await message.answer('\n'.join(text))
    media_path = fr"{MEDIA_ROOT}/manual.mp4"
    with open(media_path, 'rb') as video:
        await message.answer_video(video)
