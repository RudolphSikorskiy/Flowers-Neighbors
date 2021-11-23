from django.core.management.base import BaseCommand
from aiogram import executor
from telegram_config.loader import dp
from telegram_config import middlewares, filters, handlers
from telegram_config.middlewares import setup
from telegram_config.utils.notify_admins import on_startup_notify
from telegram_config.utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    setup(dispatcher)


class Command(BaseCommand):
    help = 'Телеграм бот'

    def handle(self, *args, **options):
        executor.start_polling(dp, on_startup=on_startup)
