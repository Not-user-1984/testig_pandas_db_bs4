from datetime import date
from typing import List
from domain.models.trading import TradingResult
from domain.services.trading_service import TradingService
from datetime import date
from pydantic import BaseModel


# class DateResponse(BaseModel):
#     date: date


class TradingAppService:
    def __init__(self, trading_service: TradingService):
        self.trading_service = trading_service

    async def get_last_trading_dates(self, limit: int) -> List[date]:
        return await self.trading_service.get_last_trading_dates(limit)

    async def get_dynamics(
        self,
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
        start_date: date,
        end_date: date,
    ) -> List[TradingResult]:
        return await self.trading_service.get_dynamics(
            oil_id, delivery_type_id, delivery_basis_id, start_date, end_date
        )

    async def get_trading_results(
        self, oil_id: str, delivery_type_id: str, delivery_basis_id: str
    ) -> List[TradingResult]:
        return await self.trading_service.get_trading_results(
            oil_id, delivery_type_id, delivery_basis_id
        )