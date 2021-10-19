from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from telegram_config.inline_timepicker import InlineTimepicker

inline_timepicker = InlineTimepicker()

create_order = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать заказ')
        ],
    ],
    resize_keyboard=True
)

COSTS_FILTERS = {
    0: ('до 1000 рублей', 0, 1000),
    1: ('от 1000 до 1500 рублей', 1000, 1500),
    2: ('от 1500 до 3000 рублей', 1500, 3000),
    3: ('от 3000 до 5000 рублей', 3000, 5000),

}

chose_cost = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=COSTS_FILTERS[0][0])
        ],
        [
            KeyboardButton(text=COSTS_FILTERS[1][0])
        ],
        [
            KeyboardButton(text=COSTS_FILTERS[2][0])
        ],
        [
            KeyboardButton(text=COSTS_FILTERS[3][0])
        ],
    ],
    resize_keyboard=True
)


def products(data):
    columns = len(data) / 3
    buttons = []
    for item in data:
        buttons.append(
            [
                KeyboardButton(text=f'{item["id"]}, '
                                    f'{item["name"]} '
                                    f'{item["price"]} руб.'
                               )
            ]
        )
    buttons.append([KeyboardButton(text='Выбрать другой ценовой диапазон')])
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )


def key_builder(data, key):
    buttons = []
    for item in data:
        buttons.append(
            [
                KeyboardButton(text=f'{item[key]}')
            ]
        )
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )


def key_builder_stores(data):
    buttons = []
    for item in data:
        buttons.append(
            [
                KeyboardButton(
                    text=f'№{item["id"]}, {item["name"]}, {item["city"]}, ул,{item["street"]}, дом {item["house"]}'),
            ]
        )
    buttons.append([KeyboardButton(text='Выбрать другой город')])
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )


times = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=r'08:00')
        ],
        [
            KeyboardButton(text=r'09:00')
        ],
        [
            KeyboardButton(text=r'20:00')
        ],
        [
            KeyboardButton(text=r'21:00')
        ],
    ],
    resize_keyboard=True
)

delivery_point = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Передать текущие координаты телефона', request_location=True)
        ],
    ],
    resize_keyboard=True
)

contact = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Передать номер телефона', request_contact=True)
        ],
    ],
    resize_keyboard=True
)

confirm_order = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Подтвердить')
        ],
        [
            KeyboardButton(text=r'Исправить заказ')
        ]
    ],
    resize_keyboard=True
)

if __name__ == '__main__':

    for item in COSTS_FILTERS.keys():
        if 'от 1000 до 1500 рублей' in COSTS_FILTERS[item][0]:
            print(COSTS_FILTERS[item][0])
        else:
            print('not ok')
