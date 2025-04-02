import pytest

from domain.models import CalcResult, Operation
from repositories.calc_repository import CalcRepository


@pytest.fixture()
def calc_repository(app, auto_rollback_session) -> CalcRepository:
    return app.container.calc_repository()


@pytest.mark.asyncio
async def test_add_calc_result(calc_repository):
    calc_result = CalcResult(id=1, a=1, b=2, op=Operation.ADD, result=3)
    await calc_repository.add(calc_result)

    res = await calc_repository.get(a=1, b=2, op=Operation.ADD)
    assert res == calc_result


@pytest.mark.asyncio
async def test_get_non_existent_calc_result(calc_repository):
    res = await calc_repository.get(a=1, b=2, op=Operation.ADD)
    assert res is None
