import datetime
from typing import Annotated
from uuid import uuid4
from aiogram import methods
from fastapi import APIRouter, Depends, Response, status
from pydantic import UUID4, BaseModel
from pydantic_core.core_schema import plain_serializer_function_ser_schema
from remnawave_api import RemnawaveSDK
from remnawave_api.models import CreateUserRequestDto, TelegramUserResponseDto, UpdateUserRequestDto, UserResponseDto
from database.database import DataBase
from database.models.user import User
from models.users import UserResponse, CreateUserRequest, AddDaysRequest
from services.admin.service import AdminService


class Users():
    def __init__(self,
                 r_sdk : RemnawaveSDK,
                 db: DataBase,
                 admin_service: AdminService) -> None:
        self.router = APIRouter(prefix = "/users",
                   tags = ["users"])

        self.r_sdk = r_sdk
        self.db = db
        self.admin_service = admin_service

        self.router.add_api_route(path = "/{tg_id}",endpoint=self.get_user,methods = ["get"])
        self.router.add_api_route(path = "/{tg_id}",endpoint=self.create_user,methods=["post"])
        self.router.add_api_route(path = "/add_days/{tg_id}",endpoint=self.add_days,methods=["patch"])
        self.router.add_api_route(path = "/sublink/{tg_id}", endpoint=self.get_sublink,methods=["get"])


    async def get_db_user(self,tg_id) -> User | None:
        async with self.db.session() as s:
            return await User.get(s,tg_id = tg_id)
    
    async def get_remna_user(self,tg_id) -> UserResponseDto | None: 
        db_user = await self.get_db_user(tg_id)
        if not db_user:
            return 
        uuid = db_user.uuid

        remna_user = await self.r_sdk.users.get_user_by_uuid(uuid = str(uuid))
        if not isinstance(remna_user,UserResponseDto):
            return
        if not isinstance(remna_user.expire_at,datetime.datetime):
            return
        return remna_user



    async def get_user(self,tg_id: int) -> UserResponse | None:
        db_user = await self.get_db_user(tg_id)
        if not db_user:
            return 
        remna_user = await self.get_remna_user(tg_id)
        if not remna_user:
            return

        await self.admin_service.get_user(db_user)

        return UserResponse(tg_id=tg_id,
                            expire_at=remna_user.expire_at,
                            uuid = remna_user.uuid)


    async def create_user(self,tg_id: int) -> UserResponse | None:
        user = await self.r_sdk.users.create_user(CreateUserRequestDto(
            username = str(tg_id),
            telegram_id= tg_id,
            expire_at= datetime.datetime.now(tz = datetime.UTC),
            activate_all_inbounds=True,
        ))

        if not isinstance(user,UserResponseDto):
            return 

        if not isinstance(user.expire_at,datetime.datetime):
            return

        async with self.db.session() as s:
            dbuser = await User.create(s,tg_id=tg_id,uuid = user.uuid)

        await self.admin_service.create_user(dbuser)

        return UserResponse(
            tg_id = tg_id,
            expire_at=user.expire_at,
            uuid = user.uuid
        )

    async def add_days(self,tg_id: int,days: int )-> UserResponse | None:
        user = await self.get_user(tg_id = tg_id)
        db_user = await self.get_db_user(tg_id)
        if not user:
            return

        now = datetime.datetime.now(tz = datetime.UTC)

        if now > user.expire_at:
            to_add = now 
        else:
            to_add = user.expire_at

        user = await self.r_sdk.users.update_user(UpdateUserRequestDto(
            uuid = str(user.uuid),
            expire_at=to_add + datetime.timedelta(days = days)
        ))
        
        if not isinstance(user,UserResponseDto):
            return 

        await self.admin_service.add_days(db_user,days)

        return UserResponse(tg_id = tg_id ,expire_at=user.expire_at,uuid = user.uuid)

    async def get_sublink(self,tg_id: int) -> str | None:
        db_user = await self.get_db_user(tg_id)
        if not db_user:return
        remna_user = await self.get_remna_user(tg_id)
        if not remna_user:return

        sublink = remna_user.subscription_url
        await self.admin_service.get_sublink(db_user,sublink)
        return sublink 

