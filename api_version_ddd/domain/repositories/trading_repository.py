from abc import ABC, abstractmethod
from datetime import date
from typing import List
from domain.models.trading import TradingResult


class TradingRepository(ABC):
    @abstractmethod
    async def get_last_trading_dates(self, limit: int) -> List[date]:
        pass

    @abstractmethod
    async def get_dynamics(
        self,
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
        start_date: date,
        end_date: date,
    ) -> List[TradingResult]:
        pass

    @abstractmethod
    async def get_trading_results(
        self, oil_id: str, delivery_type_id: str, delivery_basis_id: str
    ) -> List[TradingResult]:
        pass
