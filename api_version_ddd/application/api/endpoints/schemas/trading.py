from pydantic import BaseModel
from datetime import date
from typing import List
from domain.models.trading import TradingResult


class TradingDatesResponseSchema(BaseModel):
    dates: List[date]


class TradingDynamicsResponseSchema(BaseModel):
    results: List[TradingResult]


class TradingResultsResponseSchema(BaseModel):
    results: List[TradingResult]


class ErrorSchema(BaseModel):
    error: str
