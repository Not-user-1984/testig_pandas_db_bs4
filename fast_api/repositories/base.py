from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date

from schemas.trading import TradingResult


class BaseRepository(ABC):
    @abstractmethod
    async def get_last_trading_dates(self, limit: int = 10) -> List[date]:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def get_trading_results(
        self,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[TradingResult]:
        pass

    @abstractmethod
    async def get_total_count(
        self,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
    ) -> int:
        pass