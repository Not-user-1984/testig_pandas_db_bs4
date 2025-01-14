from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from database.models.trading import SpimexTradingResults
from repositories.base import BaseRepository


class SQLTradingRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_last_trading_dates(self, limit: int = 10) -> List[date]:
        result = await self.session.execute(
            select(SpimexTradingResults.date)
            .distinct()
            .order_by(SpimexTradingResults.date.desc())
            .limit(limit)
        )
        return [row[0] for row in result.all()]

    async def get_dynamics(
        self,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[SpimexTradingResults]:
        query = select(SpimexTradingResults)

        if oil_id:
            query = query.where(SpimexTradingResults.oil_id == oil_id)
        if delivery_type_id:
            query = query.where(
                SpimexTradingResults.delivery_type_id == delivery_type_id
            )
        if delivery_basis_id:
            query = query.where(
                SpimexTradingResults.delivery_basis_id == delivery_basis_id
            )
        if start_date:
            query = query.where(SpimexTradingResults.date >= start_date)
        if end_date:
            query = query.where(SpimexTradingResults.date <= end_date)

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_trading_results(
        self,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[SpimexTradingResults]:
        query = select(SpimexTradingResults)

        if oil_id:
            query = query.where(SpimexTradingResults.oil_id == oil_id)
        if delivery_type_id:
            query = query.where(
                SpimexTradingResults.delivery_type_id == delivery_type_id
            )
        if delivery_basis_id:
            query = query.where(
                SpimexTradingResults.delivery_basis_id == delivery_basis_id
            )

        query = (
            query.order_by(SpimexTradingResults.date.desc()).offset(skip).limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_total_count(
        self,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
    ) -> int:
        query = select(func.count()).select_from(SpimexTradingResults)

        if oil_id:
            query = query.where(SpimexTradingResults.oil_id == oil_id)
        if delivery_type_id:
            query = query.where(
                SpimexTradingResults.delivery_type_id == delivery_type_id
            )
        if delivery_basis_id:
            query = query.where(
                SpimexTradingResults.delivery_basis_id == delivery_basis_id
            )

        result = await self.session.execute(query)
        return result.scalar()
