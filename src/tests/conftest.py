from contextlib import asynccontextmanager
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

from app import app as fastapi_app


@pytest.fixture(scope="session")
def db_test_container():
    with PostgresContainer("postgres:17.4", driver="asyncpg") as db:
        root_dir = Path(__file__).parent.parent
        alembic_cfg_location = root_dir / "alembic.ini"
        alembic_script_location = root_dir / "migrations"

        test_db_url = URL.create(
            drivername="postgresql+asyncpg",
            username=db.username,
            password=db.password,
            host=db.get_container_host_ip(),
            port=db.get_exposed_port(5432),
            database=db.dbname,
        )

        with patch("db.db_url", test_db_url):
            alembic_cfg = AlembicConfig(alembic_cfg_location)
            alembic_cfg.set_main_option("script_location", str(alembic_script_location))
            command.upgrade(alembic_cfg, "head")
        yield db


@pytest.fixture
def app():
    yield fastapi_app


@pytest_asyncio.fixture
async def auto_rollback_session(app, db_test_container):
    engine = create_async_engine(db_test_container.get_connection_url())

    session = async_sessionmaker(engine, expire_on_commit=False)()

    session.commit = AsyncMock(side_effect=session.flush)

    @asynccontextmanager
    async def get_db():
        yield session

    with app.container.get_db.override(get_db):
        yield

    await session.rollback()
    await session.close()
    await engine.dispose()
