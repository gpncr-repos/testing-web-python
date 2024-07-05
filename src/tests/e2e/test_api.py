import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.fixture
def client(app, auto_rollback_session):
    return TestClient(app)


def test_calc_success(client):
    data = {"a": 123, "b": 456, "op": "+"}

    result = client.post(url="/calc", json=data)

    assert result.status_code == status.HTTP_200_OK
    assert result.json() == 579


def test_calc_unknown_operation(client):
    data = {"a": 32, "b": 8, "op": "^"}

    result = client.post(url="/calc", json=data)

    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
