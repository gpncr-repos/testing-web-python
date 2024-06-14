from dependency_injector import containers, providers

from repositories.calc_repository import CalcRepository
from services.calc_service import CalcService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["api.router"])
    calc_repository = providers.Factory(CalcRepository)
    calc_service = providers.Factory(CalcService, repository=calc_repository)
