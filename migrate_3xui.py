import asyncio
from datetime import datetime
import logging
import uuid

from remnawave_api import RemnawaveSDK
from remnawave_api.models import UserResponseDto
from remnawave_api.models.users import CreateUserRequestDto
from sqlalchemy import text

from config import load_config, Config ,DatabaseConfig

from modules.database.database import DataBase
from modules.database.models.user import User
from modules.logger import logger as l

old_db_config = DatabaseConfig(
    HOST        = '176.126.103.168',
    PORT        = 5432,
    NAME        = "postgres",
    USERNAME    = "postgres",
    PASSWORD    = "pinkgwagon"

)

new_db_config = DatabaseConfig(
    HOST = "172.18.0.9",
    PORT = 5432,
    NAME = "postgres",
    USERNAME = "sosapostres",
    PASSWORD=  "raufartem777"
)


async def get_old_users(db : DataBase):
    async with db.session() as s:
        res = await s.execute(text("select * from users"))
        all = res.fetchall()
    return all

async def reg_in_remna(user,r_sdk : RemnawaveSDK,logger):
    inbound_uuids = ['a573b408-a452-4409-850f-9b66a06434b2',
                        '578ef17e-ef67-4c3a-9f35-9f33a0aab7a6',
                        '3acf6d7a-4903-4a4b-bf49-7baed581aded',
]

    expire_at = datetime.fromtimestamp(user.expiry_time/1000)
    print(user.user_id, expire_at)
    try:
        res = await r_sdk.users.create_user(
            CreateUserRequestDto(
            username             = str(user.user_id),
            telegram_id          = user.user_id,
            short_uuid           = user.sub_id,
            expire_at            = expire_at,
            active_user_inbounds = inbound_uuids
            )
        )
        return res
    except Exception as e:
        logger.error(e)

async def reg_in_new_db(user,db,res: UserResponseDto):
    async with db.session() as s:
        await User.create(s,
                            tg_id = user.user_id,
                            uuid = res.uuid,
                            invited_by = user.invited_by,
                            referrals = user.referrals,
                            firsttime_used = True,
                            registered_at = user.registered_at
                          
                            
                          )

async def main():
    config : Config= load_config()
    config.database.url
    l.setup_logging(config.logging)
    logger = logging.getLogger(__name__)

    logger.info("initializing new db")
    new_db = DataBase(new_db_config)
    await new_db.initialize()
    logger.info("new db initialized")

    old_db = DataBase(old_db_config) 
    logger.info ('old db initialized')


    r_sdk = RemnawaveSDK(   base_url  = config.remnawave.PANEL_URL,
                            token     = config.remnawave.TOKEN)


    old_users = await get_old_users(old_db)
    #new_users = await get_old_users(new_db)

    for i in old_users:
        try:
            res = await reg_in_remna(i,r_sdk,logger)
            await reg_in_new_db(i,new_db,res)
            logger.info(f"user {i.user_id} moved succes ")
        except Exception as e:
            logger.error(e)

if __name__ == "__main__":
    asyncio.run(main())







