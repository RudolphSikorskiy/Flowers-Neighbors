from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from telegram_config.data.config import ADMIN_ID
from telegram_config.loader import dp
from telegram_config.utils.db_api import db_commands
import logging

log = logging.getLogger(__name__)


async def check_customer(message: types.Message):
    answer = message.text
    fullname = message.from_user.full_name
    username = message.from_user.username
    telegram_id = message.from_user.id
    try:
        await db_commands.add_customer(fullname=fullname, username=username, telegram_id=telegram_id)
    except Exception as err:
        log.error(f'{err}')
        log.error(f'telegram_id={telegram_id}, {fullname}, {username}')
    else:
        customer = await db_commands.select_customer(telegram_id=telegram_id)
        await dp.bot.send_message(ADMIN_ID,
                                  f"Команда {answer} от пользователя:\n"
                                  f"ID: <code>{customer['customer_id']}</code>\n"
                                  f"Telegram ID: <code>{customer['telegram_id']}</code>\n"
                                  f"Имя: <code>{customer['full_name']}</code>\n"
                                  f"Username: <code>{customer['username']}</code>\n"
                                  f"Телефон: <code>{customer['phone']}</code>\n"
                                  )


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    fullname = message.from_user.full_name
    username = message.from_user.username
    telegram_id = message.from_user.id
    await check_customer(message)
    await message.answer(f'Привет, {message.from_user.full_name}!\nИспользуй /order чтобы сделать заказ')
