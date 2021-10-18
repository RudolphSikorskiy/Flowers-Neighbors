from aiogram.dispatcher.filters.state import StatesGroup, State


class Funnel(StatesGroup):
    delivery_address = State()
    price_range = State()
    chose_product = State()
    set_date = State()
    set_time = State()
    contact_phone = State()
    is_order_confirm = State()
    order_confirm = State()

