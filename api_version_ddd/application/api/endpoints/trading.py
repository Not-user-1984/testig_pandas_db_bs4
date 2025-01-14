from fastapi import APIRouter, Depends
from typing import List
from datetime import date, datetime
from pydantic import BaseModel
from application.services.trading_app_service import TradingAppService

router = APIRouter()


# Модель Pydantic для ответа
class TradingResult(BaseModel):
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: int
    count: int
    date: date
    created_on: datetime
    updated_on: datetime


@router.get("/trading/dates", response_model=None)
async def get_last_trading_dates(
    limit: int, trading_app_service: TradingAppService = Depends()
):
    return await trading_app_service.get_last_trading_dates(limit)


@router.get("/trading/dynamics", response_model=List[TradingResult])
async def get_dynamics(
    oil_id: str,
    delivery_type_id: str,
    delivery_basis_id: str,
    start_date: date,
    end_date: date,
    trading_app_service: TradingAppService = Depends(),
):
    return await trading_app_service.get_dynamics(
        oil_id, delivery_type_id, delivery_basis_id, start_date, end_date
    )


@router.get("/trading/results", response_model=List[TradingResult])
async def get_trading_results(
    oil_id: str,
    delivery_type_id: str,
    delivery_basis_id: str,
    trading_app_service: TradingAppService = Depends(),
):
    return await trading_app_service.get_trading_results(
        oil_id, delivery_type_id, delivery_basis_id
    )
