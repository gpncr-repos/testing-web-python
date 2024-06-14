from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi.params import Depends

from api.schemas import CalcRequest
from di import Container
from services.calc_service import CalcService

router = APIRouter()


@router.post("/calc")
@inject
async def calc(
    calc_request: CalcRequest,
    calc_service: CalcService = Depends(Provide[Container.calc_service]),
) -> int | float:
    return calc_service.calc(calc_request.a, calc_request.b, calc_request.op)
