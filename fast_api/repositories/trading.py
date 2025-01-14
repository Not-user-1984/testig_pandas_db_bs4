from typing import List, Optional
from datetime import date
from schemas.trading import TradingResult
from repositories.base import BaseRepository

class TradingRepository(BaseRepository):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def get_last_trading_dates(self, limit: int = 10) -> List[date]:
        return await self.repository.get_last_trading_dates(limit)

    async def get_dynamics(
        self,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[TradingResult]:
        return await self.repository.get_dynamics(
            oil_id=oil_id,
            delivery_type_id=delivery_type_id,
            delivery_basis_id=delivery_basis_id,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit,
        )

    async def get_trading_results(
        self,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[TradingResult]:
        return await self.repository.get_trading_results(
            oil_id=oil_id,
            delivery_type_id=delivery_type_id,
            delivery_basis_id=delivery_basis_id,
            skip=skip,
            limit=limit,
        )

    async def get_total_count(
        self,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
    ) -> int:
        return await self.repository.get_total_count(
            oil_id=oil_id,
            delivery_type_id=delivery_type_id,
            delivery_basis_id=delivery_basis_id,
        )