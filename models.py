from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import Base
from logger import logger


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    language = Column(String, nullable=False, default="en")
    created_at = Column(DateTime, default=utc_now, nullable=False)

    @classmethod
    async def create(cls, session: AsyncSession, **data) -> "User":
        user = cls(**data)
        session.add(user)
        try:
            await session.flush()  # id va boshqa autogen maydonlarni olish uchun
            logger.info("User flush commit", user_id=user.id)
            return user
        except SQLAlchemyError as e:
            logger.error("Error creating user", error=str(e))
            raise


    @classmethod
    async def get_user(cls, session: AsyncSession, user_id: int) -> Optional["User"]:
        result = await session.execute(select(cls).where(cls.id == user_id))
        return result.scalar_one_or_none()

    @classmethod
    async def update_user(
            cls,
            session: AsyncSession,
            user_id: int,
            **fields
    ) -> Optional["User"]:
        user = await cls.get_user(session, user_id)
        if not user:
            return None
        for k, v in fields.items():
            setattr(user, k, v)
        await session.flush()
        logger.info("User updated", user_id=user.id, updated_fields=list(fields.keys()))
        return user
