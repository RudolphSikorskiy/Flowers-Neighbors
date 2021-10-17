from aiogram.dispatcher.filters.state import StatesGroup, State


class ExampleFMS(StatesGroup):
    start = State()
    iter_1 = State()
    iter_2 = State()
    iter_3 = State()
    iter_4 = State()
    iter_5 = State()
    finfsh = State()
