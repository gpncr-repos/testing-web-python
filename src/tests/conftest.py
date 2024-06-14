import pytest

from app import app as fastapi_app


@pytest.fixture
def app():
    yield fastapi_app
