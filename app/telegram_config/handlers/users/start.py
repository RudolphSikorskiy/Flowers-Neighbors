import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from telegram_config.data.config import ADMIN_ID
from telegram_config.loader import dp
from telegram_config.utils.db_api import db_commands
from telegram_config.utils.misc import rate_limit

log = logging.getLogger(__name__)


async def check_customer(message: types.Message, state=None):
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
                                  f"In: <code>{answer}</code>\n"
                                  f"Customer <code>{customer['customer_id']}</code> "
                                  f"<code>{customer['telegram_id']}</code>\n"
                                  f"Имя: <code>{customer['full_name']}</code>\n"
                                  f"State : <code>{state}</code>\n"
                                  # f"Username: <code>{customer['username']}</code>\n"
                                  # f"Телефон: <code>{customer['phone']}</code>\n"
                                  )


@rate_limit(10, 'help')
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await check_customer(message)
    await message.answer(f'Привет, {message.from_user.full_name}!\nИспользуй /order чтобы сделать заказ')
    # TODO check_FSM for each customer
    # fullname = message.from_user.full_name
    # username = message.from_user.username
    # telegram_id = message.from_user.id
    # fsm = FSMContext(storage, 319555949, 319555949)
    # fsm2 = FSMContext(storage, 1437069793, 1437069793)
    # log.info(f'from {telegram_id}: about 319555949 {await fsm.get_state()}')
    # log.info(f'from {telegram_id}: about 319555949 {await fsm.get_data()}')
    # log.info(f'from {telegram_id}: about 1437069793 {await fsm2.get_state()}')
    # log.info(f'from {telegram_id}: about 1437069793 {await fsm2.get_data()}')
