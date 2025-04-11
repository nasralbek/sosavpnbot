from modules.bot import vpnBot
from modules.db import DB
import asyncio



async def main():
    db = DB()
    await db.start()
    bot = vpnBot()
    await bot.start()

if __name__=="__main__":
    asyncio.run(main())