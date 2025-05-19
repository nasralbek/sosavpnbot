import logging
from datetime import datetime

from typing import Any, Self



from sqlalchemy import func 
from sqlalchemy import String,Null
from sqlalchemy import select,update
from sqlalchemy.orm import Mapped, mapped_column ,relationship,selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from . import Base

logger = logging.getLogger(__name__)

class User(Base):
    __tablename__ = "users"
    
    id              : Mapped[int]       = mapped_column(primary_key=True,autoincrement=True)
    tg_id           : Mapped[int]       = mapped_column(unique     =True,nullable=False)
    sub_id          : Mapped[str]       = mapped_column(String(36), unique = True,nullable=False)
    invited_by      : Mapped[int | None]       = mapped_column(nullable=True )
    referrals       : Mapped[int]       = mapped_column(default = 0)
    username        : Mapped[str]       = mapped_column(String(length=32))
    expiry_time     : Mapped[datetime]  = mapped_column(default=func.now(), nullable=False)
    registered_at   : Mapped[datetime]  = mapped_column(default=func.now(), nullable=False)
    is_trial_used   : Mapped[bool]      = mapped_column(default=False, nullable=False)
    transactions    : Mapped[list["Transaction"]] = relationship("Transaction", back_populates="user") 

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, tg_id={self.tg_id}, sub_id='{self.sub_id}', "
            f"username='{self.username}', registered_at={self.registered_at},"
            f"expiry_time={self.expiry_time})>"
        )
    @classmethod
    async def get(cls, session: AsyncSession, tg_id: int) -> Self | None:

        filter = [User.tg_id == tg_id]
        query = await session.execute(
            select(User)
            .options(
                selectinload(User.transactions),
            )
            .where(*filter)
        )
        user = query.scalar_one_or_none()

        if user:
            logger.debug(f"User {tg_id} retrieved from the database.")
            return user

        logger.debug(f"User {tg_id} not found in the database.")
        return None
    
    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[Self]:
        query = await session.execute(select(User).options(selectinload(User.server)))
        return query.scalars().all()
    
    @classmethod
    async def create(cls, session: AsyncSession, tg_id: int, **kwargs: Any) -> Self | None:
        user = await User.get(session=session, tg_id=tg_id)

        if user:
            logger.warning(f"User {tg_id} already exists.")
            return None

        user = User(tg_id=tg_id, **kwargs)
        session.add(user)

        try:
            await session.commit()
            logger.debug(f"User {tg_id} created.")
            return user
        except IntegrityError as exception:
            await session.rollback()
            logger.error(f"Error occurred while creating user {tg_id}: {exception}")
            return None

    @classmethod
    async def update(cls, session: AsyncSession, tg_id: int, **kwargs: Any) -> Self | None:
        user = await User.get(session=session, tg_id=tg_id)

        if user:
            filter = [User.tg_id == tg_id]
            await session.execute(update(User).where(*filter).values(**kwargs))
            await session.commit()
            logger.debug(f"User {tg_id} updated.")
            return user

        logger.warning(f"User {tg_id} not found in the database.")
        return None
    
    @classmethod
    async def exists(cls, session: AsyncSession, tg_id: int) -> bool:
        return await User.get(session=session, tg_id=tg_id) is not None

    @classmethod
    async def update_trial_status(cls, session: AsyncSession, tg_id: int, used: bool) -> bool:
        """
        Updates the trial status of a user.

        Args:
            session (AsyncSession): Database session.
            tg_id (int): Telegram user ID.
            used (bool): Whether the trial has been used.

        Returns:
            bool: True if updated, False otherwise.
        """
        user = await cls.get(session=session, tg_id=tg_id)

        if not user:
            logger.warning(f"User {tg_id} not found to update trial status.")
            return False

        await session.execute(
            update(User).where(User.tg_id == tg_id).values(is_trial_used=used)
        )
        await session.commit()
        logger.info(f"Trial status updated for user {tg_id}: {used}")
        return True