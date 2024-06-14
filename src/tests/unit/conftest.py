import pytest

from domain.models import CalcResult, Operation
from repositories.calc_repository import AbstractRepository


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
def container(app):
    with app.container.calc_repository.override(FakeCalcRepository()):
        yield app.container
