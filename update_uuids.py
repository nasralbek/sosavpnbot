import remnawave_api
from environs import Env
import asyncio

from config import DatabaseConfig, load_config, load_database_config
from remnawave_api.models import TelegramUserResponseDto

from modules.database.database import DataBase
from modules.database.models.user import User



r_sdk = remnawave_api.RemnawaveSDK(
    base_url = "https://api.mysosa.xyz",
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiNGUwY2NjZGQtM2JkNS00ZDE1LTk0OGMtMWMwMmUwNTM5OGZiIiwidXNlcm5hbWUiOm51bGwsInJvbGUiOiJBUEkiLCJpYXQiOjE3NTQzNDY3NDMsImV4cCI6MTAzOTQyNjAzNDN9.3z8_ACKlXx4M_XmVIgt5iTOD0jk403ibUX9o5uIbMNA"


)


env = Env()
env.read_env()


db_config = load_database_config(env)
db_config.HOST = "localhost"
database = DataBase(db_config)
failed = []
async def main():

    k=0
    async with database.session() as s:
        users = await User.get_all(session = s) 
    
    for user in users:
        try:
            tg_id = user.tg_id
            remna_user = await r_sdk.users.get_users_by_telegram_id(tg_id.__str__())
            if not isinstance(remna_user,TelegramUserResponseDto):
                not_inst_users.append(remna_user)
                continue
            
            await User.update(session = s,tg_id = tg_id ,uuid =  remna_user.response[0].uuid)

            print(f"{k} - {tg_id}:{user.uuid} -> {remna_user.response[0].uuid}")

            k+=1
        except Exception as e:
            print(f"exception {e} for tg_id = {tg_id}")
            failed.append(tg_id)

    print(failed)
if __name__ == "__main__":
    asyncio.run(main())
