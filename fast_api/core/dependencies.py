from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database.unit_of_work import get_session
from repositories.base import BaseRepository
from infra.sql_raw.trading import TradingRepositoryImpl
from infra.sql.trading import SQLTradingRepository
from repositories.trading import TradingRepository
from services.trading import TradingService


async def get_sql_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLTradingRepository:
    return SQLTradingRepository(session)


async def get_trading_repository(
    sql_repo: SQLTradingRepository = Depends(get_sql_repository),
) -> BaseRepository:
    return TradingRepository(sql_repo)

# async def get_trading_repository() -> BaseRepository:
#     pg_repo = TradingRepositoryImpl()
#     return TradingRepository(pg_repo)

async def get_trading_service(
    repo: TradingRepository = Depends(get_trading_repository),
) -> TradingService:
    return TradingService(repo)