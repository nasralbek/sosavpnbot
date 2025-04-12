from modules.bot import vpnBot
from modules.db import DB
import asyncio

async def main():
    db = DB("../data/databases/db.sqlite3")
    await db.start()
    bot = vpnBot(db)
    await bot.start()

if __name__=="__main__":
    print("starting")
    asyncio.run(main())