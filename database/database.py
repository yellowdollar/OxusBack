from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

DATABASE_URI = 'postgresql+asyncpg://postgres:934007717@localhost/oxus_forum'

async_engine = create_async_engine(
    DATABASE_URI, echo = False
)

Base = declarative_base()

async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

async def init_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session