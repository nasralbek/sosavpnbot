from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker

from .database import DBSessionMiddleware
from .garbage import GarbageMiddleware
from .log import LogMiddleware
from .maintenance import MaintenanceMiddleware



def register(dispatcher: Dispatcher,session: async_sessionmaker) -> None:
    middlewares = [
        LogMiddleware(),
        MaintenanceMiddleware(),
        DBSessionMiddleware(session),
        GarbageMiddleware(),

    ]

    for middleware in middlewares:
        dispatcher.update.middleware.register(middleware)