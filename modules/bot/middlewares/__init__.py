from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker

from aiogram.utils.i18n import I18n, SimpleI18nMiddleware

from .throttling import ThrottlingMiddleware
from .database import DBSessionMiddleware
from .garbage import GarbageMiddleware
from .log import LogMiddleware
from .maintenance import MaintenanceMiddleware
from .remove import RemoveMiddleware


def register(dispatcher: Dispatcher,i18n:I18n,session: async_sessionmaker) -> None:
    middlewares = [
        ThrottlingMiddleware(),
        LogMiddleware(),
        GarbageMiddleware(),
        SimpleI18nMiddleware(i18n),
        MaintenanceMiddleware(),
        DBSessionMiddleware(session),
#        RemoveMiddleware()
    ]

    for middleware in middlewares:
        dispatcher.update.middleware.register(middleware)
