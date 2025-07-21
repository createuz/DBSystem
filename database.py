from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from logger import logger
from settings import settings

Base = declarative_base()

engine = create_async_engine(
    settings.DB_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=settings.PG_POOL_MIN_SIZE,
    max_overflow=settings.PG_POOL_MAX_SIZE,
)
logger.info("🔧 SQLAlchemy engine created", db_url=settings.DB_URL)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database initialized (tables created)")


async def dispose_db():
    await engine.dispose()
    logger.info("🛑 Database engine disposed")
