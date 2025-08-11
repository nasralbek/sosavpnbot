
import logging
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import DatabaseConfig
from . import models

# from modules.database.models.User_model import create_user_model
# from modules.database.models.Transaction_model import create_transaction_model

"""
class DatabaseManager():
    def __init__(self,db : Gino):
        self.db = db

        self.User = create_user_model(self.db)
        self.Transaction = create_transaction_model(self.db)
        
    async def init_tables(self):
        await self.db.gino.create_all()

    @classmethod
    async def auth(cls, host: str, port:str,dbname:str,login:str,password:str) -> 'DatabaseManager':
        db = Gino()
        uri = "postgresql://%s:%s@%s:%s/%s"  %  (login,    
                                                password,
                                                host,
                                                port,
                                                dbname)
        await db.set_bind(bind = uri)
        return cls(db)
    
    async def connect(self):
        if self.db_uri == None:
            raise Exception("db_uri not setted, \nyou need to set it with auth method")
        await self.db.connect(self.db_uri)
    
    async def auth_from_config():
        return await DatabaseManager.auth(PG_CONFIG.PG_HOST,
                             PG_CONFIG.PG_PORT,
                             PG_CONFIG.PG_DB_NAME,
                             PG_CONFIG.PG_USERNAME,
                             PG_CONFIG.PG_PASSWORD)
"""


logger = logging.getLogger(__name__)


class DataBase:
    def __init__(self, config: DatabaseConfig) -> None:
        self.engine = create_async_engine(
            url=config.url(),
            pool_pre_ping=True,
            pool_size = 20,
            max_overflow = 30,
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        logger.debug("Database engine and session maker initialized successfully.")

    async def initialize(self) -> Self:
        try:
            async with self.engine.begin() as connection:
                await connection.run_sync(models.Base.metadata.create_all)
            logger.debug("Database schema initialized successfully.")
        except Exception as exception:
            logger.error(f"Error initializing database schema: {exception}")
            raise
        return self

    async def close(self) -> None:
        try:
            await self.engine.dispose()
            logger.debug("Database engine closed successfully.")
        except Exception as exception:
            logger.error(f"Error closing database engine: {exception}")
            raise
