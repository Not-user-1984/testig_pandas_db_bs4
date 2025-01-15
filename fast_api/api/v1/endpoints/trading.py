from fastapi import APIRouter, Depends
from datetime import date
from typing import Optional
from repositories.base import BaseRepository
from services.trading import TradingService
from schemas.trading import TradingResultResponse
from core.dependencies import get_trading_service
from core.cache import cache_response, cache
from aiocache.serializers import PickleSerializer, JsonSerializer
from aiocache import Cache, cached

router = APIRouter(prefix="/v1/trading", tags=["trading"])


cache = Cache(Cache.REDIS, endpoint="localhost", port=6379, serializer=JsonSerializer())


@router.get("/trading_results/", response_model=list[TradingResultResponse])
@cache_response()
async def get_trading_results(
    skip: int = 0,
    limit: int = 10,
    oil_id: Optional[str] = None,
    delivery_type_id: Optional[str] = None,
    delivery_basis_id: Optional[str] = None,
    service: BaseRepository = Depends(get_trading_service),
):
    return await service.get_trading_results(
        skip=skip,
        limit=limit,
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
    )


@router.get("/dynamics/", response_model=list[TradingResultResponse])
@cache_response(expire=60 * 60)
async def get_dynamics(
    oil_id: Optional[str] = None,
    delivery_type_id: Optional[str] = None,
    delivery_basis_id: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 10,
    service: BaseRepository = Depends(get_trading_service),
):
    return await service.get_dynamics(
        oil_id=oil_id,
        delivery_type_id=delivery_type_id,
        delivery_basis_id=delivery_basis_id,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )


@router.get("/last_trading_dates/", response_model=list[date])
@cache_response(expire=60 * 60)
async def get_last_trading_dates(
    limit: int = 10,
    service: BaseRepository = Depends(get_trading_service),
):
    return await service.get_last_trading_dates(limit)
