from domain.calculator.calculator import Calculator
from domain.calculator.strategies import AddStrategy, DivStrategy, MulStrategy, SubStrategy
from domain.models import CalcResult, Operation
from repositories.calc_repository import AbstractRepository


class CalcService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    async def calc(self, a: int, b: int, op: Operation) -> int | float:
        existing = await self.repository.get(a, b, op)
        if existing:
            return existing.result
        result = self._calc(a, b, op)
        await self.repository.add(CalcResult(a=a, b=b, op=op, result=result))
        return result

    def _calc(self, a: int, b: int, op: Operation) -> int | float:
        match op:
            case Operation.ADD:
                strategy = AddStrategy()
            case Operation.SUB:
                strategy = SubStrategy()
            case Operation.MUL:
                strategy = MulStrategy()
            case Operation.DIV:
                strategy = DivStrategy()
            case _:
                raise ValueError("Unexpected operation!")
        calculator = Calculator(strategy)
        return calculator.calc(a, b)
