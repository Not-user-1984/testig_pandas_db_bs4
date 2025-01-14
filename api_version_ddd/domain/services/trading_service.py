from datetime import date
from typing import List
from domain.models.trading import TradingResult
from domain.repositories.trading_repository import TradingRepository


class TradingService:
    def __init__(self, repository: TradingRepository):
        self.repository = repository

    async def get_last_trading_dates(self, limit: int) -> List[date]:
        return await self.repository.get_last_trading_dates(limit)

    async def get_dynamics(
        self,
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
        start_date: date,
        end_date: date,
    ) -> List[TradingResult]:
        return await self.repository.get_dynamics(
            oil_id, delivery_type_id, delivery_basis_id, start_date, end_date
        )

    async def get_trading_results(
        self, oil_id: str, delivery_type_id: str, delivery_basis_id: str
    ) -> List[TradingResult]:
        return await self.repository.get_trading_results(
            oil_id, delivery_type_id, delivery_basis_id
        )