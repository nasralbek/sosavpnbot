from aiogram import Bot, Dispatcher
from aiohttp.web import Application

from . import (
    #misc,
    admin_tools,
    notification,
    main_menu,
    instruction_handler,
    #instruction_handler,
    #top_up_handler,
    connect,
    support,
    invite,
    purshare,
    select_plan,
    select_method,
    purshare_final,
    polite
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
        connect.handler.router,
        invite.handler.router,
        purshare.handler.router,
        select_plan.handler.router,
        select_method.handler.router,
        purshare_final.handler.router,
        instruction_handler.handler.router,
        admin_tools.handler.router,
        #instructions.router,
        #topup.router,
        support.handler.router,
        notification.handler.router,
        polite.handler.router
    )
