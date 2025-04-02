import abc
from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models import CalcResult, Operation


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, calc_result: CalcResult) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, a: int, b: int, op: Operation) -> CalcResult | None:
        raise NotImplementedError


class CalcRepository(AbstractRepository):
    def __init__(self, get_db: Callable):
        self.get_db = get_db

    async def add(self, calc_result: CalcResult) -> None:
        async with self.get_db() as session:
            session: AsyncSession
            session.add(calc_result)
            await session.commit()

    async def get(self, a: int, b: int, op: Operation) -> CalcResult | None:
        async with self.get_db() as session:
            session: AsyncSession
            statement = select(CalcResult).where(
                CalcResult.a == a, CalcResult.b == b, CalcResult.op == op
            )
            result = await session.scalars(statement)
            return result.first()
