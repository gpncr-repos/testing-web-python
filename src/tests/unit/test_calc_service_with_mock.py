from unittest.mock import MagicMock

import pytest

from domain.models import CalcResult, Operation
from repositories.calc_repository import CalcRepository
from services.calc_service import CalcService


@pytest.fixture
def service(app) -> CalcService:
    mock_repository = MagicMock(spec=CalcRepository)
    mock_repository.get.return_value = None
    with app.container.calc_repository.override(mock_repository):
        yield app.container.calc_service()


test_params = [
    pytest.param(10, 20, Operation.ADD, 30, id="ADD"),
    pytest.param(10, 20, Operation.SUB, -10, id="SUB"),
    pytest.param(10, 20, Operation.MUL, 200, id="MUL"),
    pytest.param(10, 20, Operation.DIV, 0.5, id="DIV"),
]


@pytest.mark.parametrize("a,b,operation,expected", test_params)
def test_calc_no_saved_result(service, a, b, operation, expected):
    result = service.calc(a, b, operation)

    assert result == expected
    assert service.repository.get.call_count == 1
    assert service.repository.add.call_count == 1


@pytest.mark.parametrize("a,b,operation,expected", test_params)
def test_calc_from_saved_result(service, a, b, operation, expected):
    service.calc(a, b, operation)

    service.repository.get.return_value = CalcResult(a=a, b=b, op=operation, result=expected)
    result = service.calc(a, b, operation)

    assert result == expected
    assert service.repository.get.call_count == 2
    assert service.repository.add.call_count == 1
