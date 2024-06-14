from enum import Enum

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Operation(str, Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"


class Base(DeclarativeBase):
    pass


class CalcResult(Base):
    __tablename__ = "calc_result"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    a: Mapped[int]
    b: Mapped[int]
    op: Mapped[Operation]
    result: Mapped[float]
