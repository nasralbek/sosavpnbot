from configs.main_config import db_filename
from modules.bot.bot import vpnBot
from modules.databases.DB_GINO_MANAGER import DatabaseManager
from modules.app_manager.app_manager import App_manager

#from modules.yookassaAPI.yookassa_handler import Yookassa_handler
import asyncio 



async def main():
    db_manager = await DatabaseManager.auth_from_config()
    await db_manager.init_tables()
    app_manager = await App_manager.get_instance()

    bot = vpnBot(db_manager,app_manager)    
    await bot.start()
    print("started")


if __name__=="__main__":
    print("starting")
    asyncio.run(main())
    print("stopped")