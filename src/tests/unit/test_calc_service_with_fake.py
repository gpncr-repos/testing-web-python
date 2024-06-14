import pytest

from domain.models import Operation
from services.calc_service import CalcService


@pytest.fixture
def service(container) -> CalcService:
    return container.calc_service()


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
    assert len(service.repository.data) == 1


@pytest.mark.parametrize("a,b,operation,expected", test_params)
def test_calc_from_saved_result(service, a, b, operation, expected):
    service.calc(a, b, operation)
    result = service.calc(a, b, operation)

    assert result == expected
    assert len(service.repository.data) == 1
