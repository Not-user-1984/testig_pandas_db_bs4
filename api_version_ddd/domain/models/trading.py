from pydantic import BaseModel
from datetime import date, datetime

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