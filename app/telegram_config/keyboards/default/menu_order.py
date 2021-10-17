from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard_constructor(data: dict):
    buttons = []
    for item in data:
        buttons.append(
            [
                KeyboardButton(text=f'{item["key_1"]}'
                                    f'{item["key_1"]}'
                                    f'{item["key_1"]}'
                               )
            ]
        )
    buttons.append([KeyboardButton(text='default  button')])
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )


if __name__ == '__main__':
    pass
