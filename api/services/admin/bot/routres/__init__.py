
from aiogram import Dispatcher
from . import admin


def include(dp : Dispatcher):
    dp.include_router(admin.router)

