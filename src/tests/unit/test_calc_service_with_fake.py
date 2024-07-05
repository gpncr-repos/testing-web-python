import pytest

from domain.models import CalcResult, Operation
from repositories.calc_repository import AbstractRepository
from services.calc_service import CalcService


class FakeCalcRepository(AbstractRepository):
    def __init__(self):
        self.data: list[CalcResult] = []

    def add(self, calc_result: CalcResult) -> None:
        self.data.append(calc_result)

    def get(self, a: int, b: int, op: Operation) -> CalcResult | None:
        for row in self.data:
            if row.a == a and row.b == b and row.op == op:
                return row
        return None


@pytest.fixture
def service(app) -> CalcService:
    with app.container.calc_repository.override(FakeCalcRepository()):
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
    assert len(service.repository.data) == 1


@pytest.mark.parametrize("a,b,operation,expected", test_params)
def test_calc_from_saved_result(service, a, b, operation, expected):
    service.calc(a, b, operation)
    result = service.calc(a, b, operation)

    assert result == expected
    assert len(service.repository.data) == 1
