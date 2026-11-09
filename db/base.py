from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/data"

engine = create_async_engine(DATABASE_URL)
Base = declarative_base()

# Используем async_sessionmaker вместо sessionmaker
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
