from pydantic import BaseModel

from domain.models import Operation


class CalcRequest(BaseModel):
    a: int
    b: int
    op: Operation
