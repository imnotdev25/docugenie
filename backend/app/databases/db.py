from typing import AsyncGenerator

import logfire
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlmodel import SQLModel

from app.config import settings

# Create async engine
engine = create_async_engine(
    settings.POSTGRES_URI,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    echo=False,
)

# Create async session maker
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    try:
        # Verify database connection
        async with engine.begin() as conn:
            await conn.run_sync(lambda _: logfire.info("Database connection successful"))
            await conn.run_sync(SQLModel.metadata.create_all)

    except Exception as e:
        logfire.error(f"Database initialization failed: {str(e)}")
        raise

async def close_db():
    try:
        await engine.dispose()
        logfire.info("Database connection closed")
    except Exception as e:
        logfire.error(f"Error closing database: {str(e)}")
        raise

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logfire.error(f"Session error: {str(e)}")
            raise
        finally:
            await session.close()
