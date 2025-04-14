from configs.main_config import db_filename
from modules.bot import vpnBot

from modules.users_db import Users_DB
from modules.transactions_db import Transactions_DB
from modules.keys_db import Keys_DB
from modules.keys_notify_db import Keys_notify_DB
from modules.reserve_keys_db import Reserve_keys_DB

from modules.yookassa_handler import Yookassa_handler
import asyncio 


async def init_databases():
    databases = (Users_DB,Transactions_DB,Keys_DB,Keys_notify_DB,Reserve_keys_DB)
    for db in databases:
        e = db(db_filename)
        await e.init_db()

async def main():
    await init_databases()
    db = Users_DB(db_filename)
    await db.start()
    bot = vpnBot(db)    
    await bot.start()


if __name__=="__main__":
    print("starting")
    asyncio.run(main())
    print("stopped")