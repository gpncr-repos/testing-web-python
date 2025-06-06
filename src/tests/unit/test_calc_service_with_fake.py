import pytest

from domain.exceptions import CannotDivideByZeroError
from domain.models import CalcResult, Operation
from repositories.calc_repository import AbstractRepository
from services.calc_service import CalcService


class FakeCalcRepository(AbstractRepository):
    def __init__(self):
        self.data: list[CalcResult] = []

    async def add(self, calc_result: CalcResult) -> None:
        self.data.append(calc_result)

    async def get(self, a: int, b: int, op: Operation) -> CalcResult | None:
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


@pytest.mark.asyncio
@pytest.mark.parametrize("a,b,operation,expected", test_params)
async def test_calc_no_saved_result(service, a, b, operation, expected):
    result = await service.calc(a, b, operation)

    assert result == expected
    assert len(service.repository.data) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("a,b,operation,expected", test_params)
async def test_calc_from_saved_result(service, a, b, operation, expected):
    await service.calc(a, b, operation)
    result = await service.calc(a, b, operation)

    assert result == expected
    assert len(service.repository.data) == 1


@pytest.mark.asyncio
async def test_calc_division_by_zero(service):
    with pytest.raises(CannotDivideByZeroError):
        await service.calc(1, 0, Operation.DIV)
