import pytest
import pytest_asyncio
from fastapi import status
from httpx import ASGITransport, AsyncClient


@pytest_asyncio.fixture()
async def client(app, auto_rollback_session):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_calc_success(client):
    data = {"a": 123, "b": 456, "op": "+"}

    result = await client.post(url="/calc", json=data)

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == 579


@pytest.mark.asyncio
async def test_calc_unknown_operation(client):
    data = {"a": 32, "b": 8, "op": "^"}

    result = await client.post(url="/calc", json=data)

    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
