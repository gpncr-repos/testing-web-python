import abc

from domain.exceptions import CannotDivideByZeroError


class AbstractCalcStrategy(abc.ABC):
    @abc.abstractmethod
    def calc(self, a: int, b: int) -> int | float:
        raise NotImplementedError


class AddStrategy(AbstractCalcStrategy):
    def calc(self, a: int, b: int) -> int | float:
        return a + b


class SubStrategy(AbstractCalcStrategy):
    def calc(self, a: int, b: int) -> int | float:
        return a - b


class MulStrategy(AbstractCalcStrategy):
    def calc(self, a: int, b: int) -> int | float:
        return a * b


class DivStrategy(AbstractCalcStrategy):
    def calc(self, a: int, b: int) -> int | float:
        if b == 0:
            raise CannotDivideByZeroError
        return a / b
