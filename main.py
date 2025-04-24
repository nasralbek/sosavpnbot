from configs.main_config import db_filename
from modules.bot import vpnBot
from modules.databases.gino.DB_GINO_MANAGER import DatabaseManager

from modules.yookassa_handler import Yookassa_handler
import asyncio 



async def main():
    PG_DB_NAME = "postgres"
    PG_USERNAME = "postgres"
    PG_PASSWORD = "changeme"
    PG_HOST = "127.0.0.1"
    PG_PORT = "5432"
    db_manager = await DatabaseManager.auth(PG_HOST,
                                            PG_PORT,
                                            PG_DB_NAME,
                                            PG_USERNAME,
                                            PG_PASSWORD)
    await db_manager.init_tables()
    bot = vpnBot(db_manager)    
    await bot.start()


if __name__=="__main__":
    print("starting")
    asyncio.run(main())
    print("stopped")