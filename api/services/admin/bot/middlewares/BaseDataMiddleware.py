


from aiogram import BaseMiddleware
from remnawave_api import RemnawaveSDK


class BaseDataMiddleware(BaseMiddleware):
    def __init__(self,r_sdk : RemnawaveSDK):
        self.r_sdk = r_sdk
        super().__init__()

    async def __call__(self, handler, event, data: dict):
        data["r_sdk"] = self.r_sdk
        return await handler(event, data)


