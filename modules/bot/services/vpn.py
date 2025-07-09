
from datetime import UTC, datetime, timedelta
import logging
from remnawave_api.exceptions import NotFoundError
from sqlalchemy.ext.asyncio import async_sessionmaker
from config import Config
from modules.database.models.user import User

from remnawave_api import RemnawaveSDK
from remnawave_api.models import CreateUserRequestDto, TelegramUserResponseDto, UpdateUserRequestDto, UsersResponseDto, UserResponseDto

logger = logging.getLogger(__name__)

class VPNService:
    def __init__(
        self,
        config: Config,
        session: async_sessionmaker,
        r_sdk: RemnawaveSDK
        #server_pool_service: ServerPoolService, TODO: MAKE
    ) -> None:
        self.config = config
        self.session = session
        self.r_sdk = r_sdk
        #self.server_pool_service = server_pool_service
        logger.info("VPN Service initialized.")

    async def get_client(self,user: User) -> UserResponseDto | None:
        client = await self.r_sdk.users.get_user_by_uuid(uuid = str(user.uuid))
        if not isinstance(client,UserResponseDto):
            logger.info(f"Client {user.tg_id} not found")
            return None
        logger.info(f"Client {user.tg_id} found")
        return client


    async def is_client_exists(self,user: User) -> bool:
        try:
            client = await self.get_client(user) 
        except NotFoundError:
            return False
        except Exception as e:
            logger.error("unpredictet response error in is_client_exists : {e}")
            return False
        return True

    async def register_user(self,user: User) -> UserResponseDto | None:
        
        try:
            client = await self.r_sdk.users.create_user(
               CreateUserRequestDto(username=str(user.tg_id),
                                    expire_at=datetime.now(tz = UTC),
                                    telegram_id=user.tg_id,
                                    activate_all_inbounds=True,
                ) 
            )
            
        except Exception as e:
            logger.exception(f"exception while registering user {user.tg_id}")
            logger.info(f"trying to get user {user.tg_id} from remna")
            client  = await self.r_sdk.users.get_users_by_telegram_id(telegram_id = str(user.tg_id))
        a = isinstance(client,UserResponseDto)
        b = isinstance(client, TelegramUserResponseDto)
        if not (a or b): 
            logger.error(f"failed to register user : {user.tg_id}")
            return None
        if b:
            return client.response[0]
        return client

    async def add_days(self,user: User, delta: timedelta) -> UsersResponseDto | None:
        client = await self.get_client(user)
        now = datetime.now(tz=UTC)
        if not isinstance(client,UserResponseDto):
            logger.error(f"failed to get user {user.tg_id} while updating expiry time")
            return
        current_expiry = client.expire_at

        if not isinstance(current_expiry,datetime):
            current_expiry = now
        if current_expiry<now:
            current_expiry=now

        new_expire_at = current_expiry + delta 

        response = await self.r_sdk.users.update_user(
            UpdateUserRequestDto(
                uuid = client.uuid,
                expire_at=new_expire_at
            )
        )
        logger.info(f"added delta to user: {user.tg_id}: {delta}")
        return response
    
    async def get_key(self,user: User) -> str  :
        client = await self.get_client(user)
        if not isinstance(client, UserResponseDto):
            logger.error(f"failed to get user : {user.tg_id} while fetching key")
            return ""
        return str(client.subscription_url)

    async def get_short_uuid(self,user: User) -> str :
        client = await self.get_client(user)
        if not isinstance(client,UserResponseDto):
            logger.error(f"failder to get user : {user.tg_id} while fetching key")
            return ""
        return str(client.short_uuid)

    async def get_remaining_time(self,user: User) -> timedelta | None:
        now = datetime.now(tz=UTC)
        expiry = await self.get_expire_at(user)
        if not isinstance(expiry,datetime):
            return
        remaining_time = expiry - now
        return remaining_time

    async def get_expire_at(self,user: User)-> datetime | None:
        client = await self.get_client(user)
 
        if not isinstance(client,UserResponseDto):
            logger.error(f"failed to get user {user.tg_id}")
            return None
        if not isinstance(client.expire_at, datetime):
            logger.error(f"failed to get user {user.tg_id}")
            return None
        
        logger.info(f"{user.tg_id} expires at {client.expire_at}")
        return client.expire_at
               
    async def set_expiry(self,user: User,new_expiry : datetime)-> UserResponseDto | None:
        client = await self.get_client(user)
        
        response = await self.r_sdk.users.update_user(
            UpdateUserRequestDto(
                uuid = client.uuid,
                expire_at=new_expiry
            )
        )
        if not isinstance(response,UserResponseDto):
            return None
        return response


