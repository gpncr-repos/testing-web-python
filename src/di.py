from dependency_injector import containers, providers

from db import get_db
from repositories.calc_repository import CalcRepository
from services.calc_service import CalcService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["api.router"])
    get_db = providers.Object(get_db)
    calc_repository = providers.Factory(CalcRepository, get_db=get_db)
    calc_service = providers.Factory(CalcService, repository=calc_repository)
