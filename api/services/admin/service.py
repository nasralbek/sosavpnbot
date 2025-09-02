import asyncio
from enum import Enum
import logging
from typing import Any

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, parse_mode
from aiogram.types import ForumTopic, Update
from pydantic import BaseModel
from remnawave_api import RemnawaveSDK
from config import AdminBotConfig
import aiogram
import traceback

from database.database import DataBase
from database.models import admin_topics 
from database.models.admin_topics import admin_topic
from database.models.transaction import Transaction
from database.models.user import User
from models.users import TransactionResponse
from services.admin.bot.middlewares.BaseDataMiddleware import BaseDataMiddleware
from services.admin.bot.middlewares.admin import AdminMiddleware
from services.admin.bot.middlewares.admin_chat import AdminChatMiddleware
from services.admin.bot.middlewares.log import LogMiddleware
from services.admin.bot.routres import include


logger = logging.getLogger(__name__)

class ADMIN_TOPIC_TAGS(str,Enum):
    USER_CREATE = "USER CREATE"
    ADD_DAYS    = "ADD DAYS"
    USER_GET    = "USER GET"
    REMNAWAVE   = "REMNAWAVE"
    GET_SUBLINK = "GET SUBLINK"
    EXCEPTIONS  = "EXCEPTIONS"
    GET_TRANSACTION = "GET TRANSACTION"
    CANCEL_TRANSACION = "CANCEL TRANSACTION"
    SUCCESS_TRANSACTION = "SUCCESS TRANSACTION"
    API_INFO = "API INFO"
    FULL_LOG = "FULL LOG"
    ADMIN_TOPIC = "ADMIN TOPIC"

SPACE = "\n"

class AdminService():
    def __init__(self,config: AdminBotConfig,db :DataBase,r_sdk: RemnawaveSDK ) -> None:
        self.config = config
        self.db = db
        self.bot : aiogram.Bot = aiogram.Bot(token = self.config.API_TOKEN,
                                default = DefaultBotProperties(
                                parse_mode=ParseMode.HTML))
        self.r_sdk = r_sdk

    async def init_topics(self):
        
        tags = [e.value for e in ADMIN_TOPIC_TAGS]
        
        self.topic_schema = {}

        async with self.db.session() as s:
            for tag in tags:
                topic = await admin_topic.get(session = s ,TAG = tag)
                if not topic:
                    created_topic : ForumTopic = await self.bot.create_forum_topic(
                                    self.config.ADMIN_CHAT_ID,
                                    name = tag)
                    topic = await admin_topic.create(session = s,
                                                     TAG = tag,
                                                     id = created_topic.message_thread_id)

                if not topic:
                    continue
                self.topic_schema[tag] = topic.id

    @staticmethod
    def _safe(foo):
        async def result(self,*args,**kwargs):
            try:
                await foo(self,*args,**kwargs)
            except Exception as e:
                logger.exception(e)
                await self.notify_exception(e,traceback.format_exc(),__name__)
        return result

    def form_base_user_information(self,user: User):
        text = f"<b>USER</b>\n"
        format_str = "<blockquote><b>%s: </b>%s</blockquote>\n"
        text += format_str % ("user_id",user.tg_id)
        text += format_str % ("username",f"@{user.username}")
        text += format_str % ("registered at",user.registered_at)
        text += format_str % ("firsttime_used",user.firsttime_used)
        text += format_str % ("uuid",user.uuid)
        text += format_str % ("invited by",user.invited_by)
        text += format_str % ("referrals",user.referrals)
        return text

    def form_base_transaction_information(self,transaction: Transaction):
        text = f"<b>TRANSACTION</b>\n"
        format_str = "<blockquote><b>%s: </b>%s</blockquote>\n"
        text += format_str %  ("payment_id",transaction.payment_id)
        text += format_str %  ("tg_id", transaction.tg_id)
        text += format_str %  ("status",transaction.status)
        text += format_str % ("days",transaction.days)
        text += format_str % ("created at", transaction.created_at)
        try:
            text += format_str % ("updated at", transaction.updated_at)
        except Exception:
            text += format_str % ("updated at", "now")
        text += self.form_base_user_information(transaction.user)
        return text

    def form_additional_data(self,data: dict):
        result = "<b>additional data</b>\n"
        for key,value in data.items():
            result+=f"<blockquote>{key}: {value}</blockquote>\n"
        return result

    async def notify_exception(self,e: Exception, 
                               tracebackmessage: str| None = None,
                               name = None):
        try:
            text = "```EXCEPTION```\n\n"
            if name:
                text +="filename:"
                text += SPACE
                text += f"```{name}```" 
                text += SPACE
            
            text += SPACE
            text += "exception type:"
            text +=  f"```{e}```" 

            if tracebackmessage:
                text += SPACE
                text += f"```{tracebackmessage}```" 
                text += SPACE

            await self.send(text,ADMIN_TOPIC_TAGS.EXCEPTIONS,parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.exception(e)

    async def send(self,text: str ,topic_tag: ADMIN_TOPIC_TAGS, **kwargs):
        await self.bot.send_message(
                chat_id=self.config.ADMIN_CHAT_ID,
                message_thread_id=self.topic_schema[topic_tag],
                text = text,
                **kwargs)
        await self.bot.send_message(
                chat_id = self.config.ADMIN_CHAT_ID,
                message_thread_id=self.topic_schema[ADMIN_TOPIC_TAGS.FULL_LOG],
                text = text,
                **kwargs)

    def form_title(self,text):
        return f"<b>{text}</b>\n\n"

    @_safe
    async def add_days(self,db_user:User,days):
        text =   self.form_title("ADD DAYS") \
                    +self.form_base_user_information(db_user) \
                    +SPACE\
                    +self.form_additional_data({"days":days})
        await self.send(text,ADMIN_TOPIC_TAGS.ADD_DAYS)
    
    @_safe
    async def get_user(self,db_user : User):
        text =  self.form_title("GET USER")\
                    +self.form_base_user_information(db_user)
        await self.send(text,ADMIN_TOPIC_TAGS.USER_GET)

    @_safe
    async def create_user(self,db_user):
        text =  self.form_title("CREATE USER") \
                    +self.form_base_user_information(db_user)
        await self.send(text,ADMIN_TOPIC_TAGS.USER_CREATE)

    @_safe
    async def get_sublink(self,db_user,sublink):
        text =  self.form_title("GET SUBLINK") \
                    +self.form_base_user_information(db_user)\
                    +self.form_additional_data({"sublink":sublink})   
        await self.send(text,ADMIN_TOPIC_TAGS.GET_SUBLINK)
            
    @_safe
    async def get_transaction(self,transaction):
        text = self.form_title("GET TRANSACTION") \
                +self.form_base_transaction_information(transaction)
        await self.send(text,ADMIN_TOPIC_TAGS.GET_TRANSACTION)

    @_safe 
    async def cancel_transaction(self,transaction):
        text = self.form_title("CANCEL TRANSACTION") \
                +self.form_base_transaction_information(transaction)
        await self.send(text,ADMIN_TOPIC_TAGS.CANCEL_TRANSACION)
        
    @_safe 
    async def success_transaction(self,transaction):
        text = self.form_title("SUCCESS TRANSACTION") \
                +self.form_base_transaction_information(transaction)
        await self.send(text,ADMIN_TOPIC_TAGS.SUCCESS_TRANSACTION)

    @_safe
    async def notify_api_started(self):
        await self.send("<b>API STARTED</b>",ADMIN_TOPIC_TAGS.API_INFO)

    @_safe
    async def notify_api_stopped(self):
        await self.send("<b>API STOPPED</b>",ADMIN_TOPIC_TAGS.API_INFO)

    def start_bot(self):
        return
        logger = logging.getLogger("uvicorn.error")

        logger.info("Starting admin bot")
        dp = aiogram.Dispatcher(r_sdk = self.r_sdk)
        include(dp)
        dp.message.middleware(LogMiddleware())
        dp.message.middleware(AdminChatMiddleware(
            int(self.config.ADMIN_CHAT_ID),
            int(self.topic_schema[ADMIN_TOPIC_TAGS.ADMIN_TOPIC])
        ))
        dp.message.middleware(AdminMiddleware(self.config.ADMINS))
        #dp.message.middleware(BaseDataMiddleware(r_sdk = self.r_sdk))

        asyncio.run (dp.start_polling(self.bot,))#allowed_updates=dp.resolve_used_update_types())

