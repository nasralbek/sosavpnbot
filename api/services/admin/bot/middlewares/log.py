


import logging
from aiogram import BaseMiddleware


logger = logging.getLogger('uvicorn.error')

class LogMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(self, handler, event, data: dict):
        #logger.info(f"Event: {event}")
        return await handler(event, data)
