from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SpimexTradingResults(Base):
    __tablename__ = "spimex_spimextradingresults"

    exchange_product_id = Column(String, primary_key=True)
    exchange_product_name = Column(String)
    oil_id = Column(String)
    delivery_basis_id = Column(String)
    delivery_basis_name = Column(String)
    delivery_type_id = Column(String)
    volume = Column(Integer)
    total = Column(Integer)
    count = Column(Integer)
    date = Column(Date)
    created_on = Column(DateTime)
    updated_on = Column(DateTime)

    def to_dict(self):
        return {
            "exchange_product_id": self.exchange_product_id,
            "exchange_product_name": self.exchange_product_name,
            "oil_id": self.oil_id,
            "delivery_basis_id": self.delivery_basis_id,
            "delivery_basis_name": self.delivery_basis_name,
            "delivery_type_id": self.delivery_type_id,
            "volume": self.volume,
            "total": self.total,
            "count": self.count,
            "date": self.date.isoformat() if self.date else None,
            "created_on": self.created_on.isoformat() if self.created_on else None,
            "updated_on": self.updated_on.isoformat() if self.updated_on else None,
        }