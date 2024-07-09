from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from api.schemas import CalcRequest
from di import Container
from domain.exceptions import CannotDivideByZeroError
from services.calc_service import CalcService

router = APIRouter()


@router.post("/calc")
@inject
async def calc(
    calc_request: CalcRequest,
    calc_service: CalcService = Depends(Provide[Container.calc_service]),
) -> int | float:
    try:
        result = calc_service.calc(calc_request.a, calc_request.b, calc_request.op)
    except CannotDivideByZeroError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exc.msg)
    return result
