

from enum import unique
import logging

from sqlalchemy import Integer, String, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, selectinload

from database.models._base import Base


logger = logging.getLogger()



class admin_topic(Base):
    __tablename__ = "admin_topics"

    tag: Mapped[str]    = mapped_column(String(length=64), unique = True,nullable=False)
    id: Mapped[int]     = mapped_column(postgresql.BIGINT, unique= True,nullable=False, primary_key=True)

    def __repr__(self) -> str:
        return super().__repr__(f"<admin_topic(id = {self.id}, tag = {self.tag})>")

    @classmethod
    async def get(cls,session: AsyncSession, TAG:str): 
        filter = [admin_topic.tag == TAG]
        query = await session.execute(
            select(admin_topic).where(*filter)
        )
        return query.scalar_one_or_none()


    @classmethod
    async def create(cls,session,TAG:str,id:int):

        topic = await admin_topic.get(session = session,TAG = TAG)

        if topic:
            logger.info("topic already exists")
            return topic

        topic = admin_topic(tag=TAG,id = id)
        session.add(topic)

        try:
            await session.commit()
            logger.debug(f"topic {TAG}:{id} created")
            return topic
        except IntegrityError as exception:
            await session.rollback()
            logger.error(f"Error occurred while creating topic {TAG}: {exception}")
            return None
