from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from telegram_config.data.config import ADMIN_ID
from telegram_config.loader import dp
from telegram_config.utils.db_api.db_commands import add_customer, select_customer
import logging

log = logging.getLogger(__name__)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    fullname = message.from_user.full_name
    username = message.from_user.username
    telegram_id = message.from_user.id
    try:
        await add_customer(fullname=fullname, username=username, telegram_id=telegram_id)
    except Exception as err:
        log.error(f'telegram_id={telegram_id}, {fullname}, {username}: {err}')
        await dp.bot.send_message(ADMIN_ID,
                                  f"К нам вернулся покупатель:\n"
                                  f"Telegram ID: <code>{telegram_id}</code>\n"
                                  f"Имя: <code>{fullname}</code>\n"
                                  f"Username: <code>{username}</code>\n"
                                  )
    else:
        customer = await select_customer(telegram_id=telegram_id)
        await dp.bot.send_message(ADMIN_ID,
                                  f"Добавлен новый покупатель:\n"
                                  f"ID: <code>{customer['customer_id']}</code>\n"
                                  f"Telegram ID: <code>{customer['telegram_id']}</code>\n"
                                  f"Имя: <code>{customer['full_name']}</code>\n"
                                  f"Username: <code>{customer['username']}</code>\n"
                                  f"Телефон: <code>{customer['phone']}</code>\n"
                                  f"Email: <code>{customer['email']}</code>\n"
                                  )

    await message.answer(f'Привет, {message.from_user.full_name}!\nИспользуй /order чтобы сделать заказ')
