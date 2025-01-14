from pydantic import BaseModel
from datetime import date

class TradingResultSchema(BaseModel):
    trade_date: date
    oil_id: str
    delivery_type_id: str
    delivery_basis_id: str
    price: float
    volume: int