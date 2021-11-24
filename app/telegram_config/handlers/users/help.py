import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from django_project.settings import MEDIA_ROOT
from telegram_config.loader import dp
from telegram_config.utils.misc import rate_limit

log = logging.getLogger(__name__)


@rate_limit(10, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать работу или перезагруить бота',
        '/order - Создать заказ',
        '/help - Получить справку с видеоинструкцией'
    ]
    await message.answer('\n'.join(text))
    media_path = fr"{MEDIA_ROOT}/manual.mp4"
    with open(media_path, 'rb') as video:
        await message.answer_video(video)
