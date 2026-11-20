import os
from typing import AsyncGenerator

from dotenv import load_dotenv

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv()

database_url = os.getenv('database_url')


if database_url is None:
    raise HTTPException(status_code=404,detail="db not found")
else:
    print("db found")

engine = create_async_engine(database_url, echo = True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    from models import Base  
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)