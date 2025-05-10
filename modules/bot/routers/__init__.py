from aiogram import Bot, Dispatcher

from . import (
    main_handlers,
    start_handler,
    instruction_handler,
    top_up_handler
)

async def include_routers(bot: Bot, dispatcher: Dispatcher, app_manager): 
    bot_me = await bot.get_me()
    bot_username = bot_me.username

    main = main_handlers.handler.Handler(app_manager,bot_username)
    start = start_handler.handler.Handler(app_manager,bot) 
    instructions = instruction_handler.handler.Handler(app_manager)
    topup = top_up_handler.handler.Handler(app_manager)


    dispatcher.include_routers(
        main.router,
        start.router,
        instructions.router,
        topup.router
    )