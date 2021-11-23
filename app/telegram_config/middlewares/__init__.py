from aiogram import Dispatcher

from .big_brother import BigBrother
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(BigBrother())
    dp.middleware.setup(ThrottlingMiddleware())
