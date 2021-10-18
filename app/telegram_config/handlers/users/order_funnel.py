from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InputFile, ReplyKeyboardMarkup
from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar

from telegram_config.keyboards.default import menu_order
from telegram_config.keyboards.default.menu_order import COSTS_FILTERS
from telegram_config.loader import dp, bot
from telegram_config.states.states import Funnel
from telegram_config.utils.db_api.db_commands import select_products, select_all_managers, select_customer, add_order
from typing import Dict
import datetime
import logging

from django_project.settings import MEDIA_ROOT

log = logging.getLogger(__name__)


@dp.message_handler(Command('order'))
async def start_order(message: Message):
    await message.answer(f"Создадим заказ\n"
                         f"Введите адрес доставки в заданном формате:\n"
                         f"<code>Садовая 21</code>.\n"
                         f"Или передайте свои координаты",
                         reply_markup=menu_order.delivery_point
                         )

    await Funnel.next()


@dp.message_handler(state=Funnel.delivery_address, content_types=types.ContentType.LOCATION)
async def set_price_range(message: Message, state: FSMContext):
    await message.answer(f"Выберите ценовой диапазон\n", reply_markup=menu_order.chose_cost)

    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    async with state.proxy() as data:
        data['delivery_address'] = (latitude, longitude)
    await Funnel.next()


@dp.message_handler(state=Funnel.delivery_address)
async def set_price_range(message: Message, state: FSMContext):
    await message.answer(f"Выберите ценовой диапазон\n", reply_markup=menu_order.chose_cost)

    answer = message.text
    async with state.proxy() as data:
        data['delivery_address'] = answer
    await Funnel.next()


@dp.message_handler(state=Funnel.price_range)
async def set_chose_product(message: Message, state: FSMContext):
    answer = message.text
    fullname = message.from_user.full_name
    username = message.from_user.username
    telegram_id = message.from_user.id

    for item in COSTS_FILTERS.keys():
        if answer in COSTS_FILTERS[item][0]:
            product = await select_products(price_from=COSTS_FILTERS[item][1], price_to=COSTS_FILTERS[item][2])
            if len(product) > 0:
                for pr in product:
                    media_path = fr"{MEDIA_ROOT}/{pr['photo']}"
                    photo_bytes = InputFile(path_or_bytesio=media_path)
                    await bot.send_photo(chat_id=telegram_id,
                                         photo=photo_bytes,
                                         caption=f'№ {pr["id"]}\n'
                                                 f'Название: <code>{pr["name"]}</code>\n'
                                                 f'Цена: <code>{pr["price"]}</code>\n'
                                                 f'Состaв: <code>{pr["description"]}</code>\n'
                                         )
                keyboard = menu_order.products(product)
                await message.answer(f"Выберите букет", reply_markup=keyboard)

                async with state.proxy() as data:
                    data['price_range'] = answer

                await Funnel.next()
            else:
                log.info(f'len product < 0 --------> {product}')


@dp.message_handler(state=Funnel.chose_product)
async def set_date(message: Message, state: FSMContext):
    answer = message.text
    if answer == 'Выбрать другой цеовой диапазон':
        await message.answer(f"Создадим заказ\n"
                             f"Введите адрес доставки в заданном формате:\n"
                             f"<code>Садовая 21</code>.\n"
                             f"Или передайте свои координаты",
                             reply_markup=menu_order.delivery_point
                             )
        await Funnel.first()
    else:
        await message.answer(f"Выбран {answer}", reply_markup=ReplyKeyboardRemove())
        async with state.proxy() as data:
            data['chosen_product'] = answer

        await message.answer("Укажите дату и время доставки: ", reply_markup=await SimpleCalendar().start_calendar())

        await Funnel.next()


@dp.callback_query_handler(simple_cal_callback.filter(), state=Funnel.set_date)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        menu_order.inline_timepicker.init(
            datetime.time(12),
            datetime.time(1),
            datetime.time(23),
        )

        await callback_query.message.answer(f'Вы выбрали {date.strftime("%d/%m/%Y")}',
                                            reply_markup=menu_order.inline_timepicker.get_keyboard())

        async with state.proxy() as data:
            data['delivery_date'] = date.strftime("%d/%m/%Y")
        await Funnel.next()


@dp.callback_query_handler(menu_order.inline_timepicker.filter(), state=Funnel.set_time)
async def set_contact_phone(query: types.CallbackQuery, callback_data: Dict[str, str],
                            state: FSMContext):
    handle_result = menu_order.inline_timepicker.handle(query.from_user.id, callback_data)

    if handle_result is not None:
        await bot.edit_message_text(f'Выбранное время {handle_result}\n',
                                    chat_id=query.from_user.id,
                                    message_id=query.message.message_id)

        await query.message.answer(f"Воспользуейтесь кнопкой 'Передать номер телефона'\n",
                                   reply_markup=menu_order.contact
                                   )
        async with state.proxy() as data:
            data['delivery_time'] = handle_result
        await Funnel.next()
    else:
        await bot.edit_message_reply_markup(chat_id=query.from_user.id,
                                            message_id=query.message.message_id,
                                            reply_markup=menu_order.inline_timepicker.get_keyboard())


@dp.message_handler(state=Funnel.contact_phone, content_types=types.ContentType.CONTACT)
async def confirming_order(message: Message, state: FSMContext):
    await message.answer(f"Подтверждение заказа:", reply_markup=menu_order.confirm_order)
    cont = message.contact

    answer = message.text
    fullname = message.from_user.full_name
    username = message.from_user.username
    telegram_id = message.from_user.id

    async with state.proxy() as data:
        data['contact'] = dict(first_name=cont.first_name, last_name=cont.last_name, phone=cont.phone_number)

    data = await state.get_data()
    await message.answer(f"Параметры заказа:\n"
                         f"Адрес доставки: <code>{data['delivery_address']}</code>\n"
                         f"Ценовой диапазон: <code>{data['price_range']}</code>\n"
                         f"Товар: <code>{data['chosen_product']}</code>\n"
                         f"Дата доставки: <code>{data['delivery_date']}</code>\n"
                         f"Время доставки: <code>{data['delivery_time']}</code>\n"
                         )

    await Funnel.next()


@dp.message_handler(state=Funnel.is_order_confirm, text="Подтвердить")
async def order_done(message: Message, state: FSMContext):
    username = message.from_user.username
    answer = message.text
    fullname = message.from_user.full_name
    username = message.from_user.username
    telegram_id = message.from_user.id

    await message.answer(f"Заказ создан, ожидайте звонка", reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    managers = await select_all_managers()

    for manag in managers:
        try:
            await dp.bot.send_message(
                manag["telegram_id"],
                f"Получен заказ:\n"
                f"Адрес доставки: <code>{data['delivery_address']}</code>\n"
                f"Ценовой диапазон: <code>{data['price_range']}</code>\n"
                f"Товар: <code>{data['chosen_product']}</code>\n"
                f"Дата доставки: <code>{data['delivery_date']}</code>\n"
                f"Время доставки: <code>{data['delivery_time']}</code>\n"
                f"Заказчик: <code>{data['contact']['first_name']}"
                f" {data['contact']['last_name']}</code>\n"
                f"Телефон: <code>{data['contact']['phone']}</code>\n"
                f"Telegram: <code>@{username}</code>"
            )

        except Exception as err:
            logging.exception(err)

    customer = await select_customer(telegram_id=telegram_id)
    await add_order(customer_id=customer,
                    product_id=data['chosen_product'].split()[0][:-1],
                    telegram_id=telegram_id,
                    shipping_address=data['delivery_address'],
                    phone_number=data['contact']['phone'],
                    email='-',
                    )

    await state.finish()


@dp.message_handler(state=Funnel.is_order_confirm, text="Исправить заказ")
async def try_again(message: Message, state: FSMContext):
    await message.answer(f"Создадим заказ\n"
                         f"Введите адрес доставки в заданном формате:\n"
                         f"<code>Садовая 21</code>.\n"
                         f"Или передайте свои координаты",
                         reply_markup=menu_order.delivery_point
                         )
    answer = message.text
    async with state.proxy() as data:
        data['order_confirmed'] = answer

    await Funnel.first()
