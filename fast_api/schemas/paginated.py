from pydantic import BaseModel
from typing import List, Optional

from schemas.trading import TradingResultResponse


class PaginatedResponse(BaseModel):
    data: List[TradingResultResponse]
    total: int
    skip: int
    limit: int
