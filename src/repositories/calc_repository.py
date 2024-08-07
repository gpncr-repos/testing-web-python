import abc
from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.models import CalcResult, Operation


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, calc_result: CalcResult) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, a: int, b: int, op: Operation) -> CalcResult | None:
        raise NotImplementedError


class CalcRepository(AbstractRepository):
    def __init__(self, get_db: Callable):
        self.get_db = get_db

    def add(self, calc_result: CalcResult) -> None:
        with self.get_db() as session:
            session: Session
            session.add(calc_result)
            session.commit()

    def get(self, a: int, b: int, op: Operation) -> CalcResult | None:
        with self.get_db() as session:
            session: Session
            statement = select(CalcResult).where(
                CalcResult.a == a, CalcResult.b == b, CalcResult.op == op
            )
            result = session.scalars(statement).first()
            return result
