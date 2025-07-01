from aiogram import Bot, Dispatcher
from aiohttp.web import Application

from . import (
    main_menu,
    #instruction_handler,
    #top_up_handler,
    profile,
    support,
    invite
)

def include(app: Application, dispatcher: Dispatcher): 
    #bot_me = await bot.get_me()
    #bot_username = bot_me.username
    bot_username = 'dsadsa'
    bot = ''

    #main = main_handlers.handler.Handler(bot_username)
    #instructions = instruction_handler.handler.Handler()
    #topup = top_up_handler.handler.Handler()


    dispatcher.include_routers(
        main_menu.handler.router,
        profile.handler.router,
        invite.handler.router,
        #instructions.router,
        #topup.router,
        support.handler.router,
    )
