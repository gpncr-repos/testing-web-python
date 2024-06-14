from domain.calculator.strategies import AbstractCalcStrategy


class Calculator:
    def __init__(self, calc_strategy: AbstractCalcStrategy):
        self.calc_strategy = calc_strategy

    def calc(self, a: int, b: int) -> int | float:
        return self.calc_strategy.calc(a, b)
