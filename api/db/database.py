from config import DBConfig

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    f"postgresql+asyncpg://{DBConfig.user}:{DBConfig.password}@{DBConfig.host}:{DBConfig.port}/{DBConfig.db_name}",
    echo=True,
)

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def initialize_database() -> None:
    """Initialize database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Get current session"""
    async with Session() as session:
        try:
            yield session
        finally:
            await session.close()


async def dispose_database() -> None:
    """Dispose database connections"""
    await engine.dispose()
