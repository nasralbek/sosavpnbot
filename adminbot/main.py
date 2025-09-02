import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from environs import Env

async def on_startup():
    env = Env()
    env.read_env()
    config = {
        "BOT_TOKEN" : env.str("ADM_BOT_TOKEN")
    }
    bot = Bot(token = config['BOT_TOKEN'],
              default = DefaultBotProperties(parse_mode="HTML"))
    dispatcher = Dispatcher()

    await dispatcher.start_polling(bot)


async def on_shutdown():
    pass


async def main():
    try:
    
        await on_startup()
    finally:
        await on_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
