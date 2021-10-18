from aiogram.dispatcher.filters.state import StatesGroup, State


class Funnel(StatesGroup):
    market = State()
    price_range = State()
    chose_product = State()
    delivery_address = State()
    set_date = State()
    set_time = State()
    contact_phone = State()
    order_confirming = State()
    is_order_confirm = State()

