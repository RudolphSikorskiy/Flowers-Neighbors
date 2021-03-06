from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить/перезагрузить бота"),
            types.BotCommand("order", "Создать заказ"),
            types.BotCommand("help", "Вывести справку"),
        ]
    )
