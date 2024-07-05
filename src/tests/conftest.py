from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest

from app import app as fastapi_app
from db import SessionLocal


@pytest.fixture
def app():
    yield fastapi_app


@pytest.fixture
def auto_rollback_session(app):
    session = SessionLocal()

    session.commit = MagicMock(side_effect=session.flush)

    @contextmanager
    def get_db():
        yield session

    with app.container.get_db.override(get_db):
        yield

    session.rollback()
    session.close()
