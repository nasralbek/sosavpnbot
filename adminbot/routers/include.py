from aiogram import Dispatcher
import main_menu 

async def include_routers(dp: Dispatcher):
    dp.include_routers(
        main_menu.router
    )

