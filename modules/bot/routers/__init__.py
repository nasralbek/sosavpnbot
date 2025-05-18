from aiogram import Bot, Dispatcher

from . import (
    main_handlers,
    start_handler,
    instruction_handler,
    top_up_handler
)

def include(app: Bot, dispatcher: Dispatcher): 
    #bot_me = await bot.get_me()
    #bot_username = bot_me.username
    bot_username = 'dsadsa'
    bot = ''

    main = main_handlers.handler.Handler(bot_username)
    start = start_handler.handler.Handler(bot) 
    instructions = instruction_handler.handler.Handler()
    topup = top_up_handler.handler.Handler()


    dispatcher.include_routers(
        main.router,
        start.router,
        instructions.router,
        topup.router
    )