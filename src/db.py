from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_scoped_session, async_sessionmaker, create_async_engine

from config import settings

db_url = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.db_user,
    password=settings.db_pass,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)
engine = create_async_engine(db_url)

AsyncScopedSession = async_scoped_session(
    async_sessionmaker(engine, expire_on_commit=False), scopefunc=current_task
)


@asynccontextmanager
async def get_db():
    db = AsyncScopedSession()
    try:
        yield db
    finally:
        await db.close()
