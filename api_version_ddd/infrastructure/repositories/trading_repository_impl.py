from datetime import date, datetime
from typing import List
import asyncpg
from domain.models.trading import TradingResult
from domain.repositories.trading_repository import TradingRepository


async def get_db_connection():
    """
    Создаёт и возвращает подключение к базе данных PostgreSQL.
    """
    connection = await asyncpg.connect(
        user="spimex_user",  # Имя пользователя
        password="spimex_password",  # Пароль
        database="spimex_db",  # Название базы данных
        host="localhost",  # Хост
        port=5432,  # Порт
    )
    return connection


class TradingRepositoryImpl(TradingRepository):
    async def get_last_trading_dates(self, limit: int) -> List[date]:
        """
        Возвращает список последних дат торгов.
        """
        connection = await get_db_connection()
        try:
            query = """
                SELECT DISTINCT date
                FROM spimex_spimextradingresults
                ORDER BY date DESC
                LIMIT $1;
            """
            rows = await connection.fetch(query, limit)
            return [row["date"] for row in rows]
        finally:
            await connection.close()

    async def get_dynamics(
        self,
        oil_id: str,
        delivery_type_id: str,
        delivery_basis_id: str,
        start_date: date,
        end_date: date,
    ) -> List[TradingResult]:
        """
        Возвращает динамику торгов за указанный период.
        """
        connection = await get_db_connection()
        try:
            query = """
                SELECT exchange_product_name, oil_id, delivery_basis_id, delivery_basis_name,
                       delivery_type_id, volume, total, count, date, created_on, updated_on
                FROM spimex_spimextradingresults
                WHERE oil_id = $1
                  AND delivery_type_id = $2
                  AND delivery_basis_id = $3
                  AND date >= $4
                  AND date <= $5
                ORDER BY date;
            """
            rows = await connection.fetch(
                query, oil_id, delivery_type_id, delivery_basis_id, start_date, end_date
            )
            return [TradingResult(**row) for row in rows]
        finally:
            await connection.close()

    async def get_trading_results(
        self, oil_id: str, delivery_type_id: str, delivery_basis_id: str
    ) -> List[TradingResult]:
        """
        Возвращает результаты торгов для указанных параметров.
        """
        connection = await get_db_connection()
        try:
            query = """
                SELECT exchange_product_name, oil_id, delivery_basis_id, delivery_basis_name,
                       delivery_type_id, volume, total, count, date, created_on, updated_on
                FROM spimex_spimextradingresults
                WHERE oil_id = $1
                  AND delivery_type_id = $2
                  AND delivery_basis_id = $3
                ORDER BY date DESC;
            """
            rows = await connection.fetch(
                query, oil_id, delivery_type_id, delivery_basis_id
            )
            return [TradingResult(**row) for row in rows]
        finally:
            await connection.close()

    async def get_all_trading_results(self) -> List[TradingResult]:
        """
        Возвращает все результаты торгов.
        """
        connection = await get_db_connection()
        try:
            query = """
                SELECT exchange_product_name, oil_id, delivery_basis_id, delivery_basis_name,
                       delivery_type_id, volume, total, count, date, created_on, updated_on
                FROM spimex_spimextradingresults
                ORDER BY date DESC;
            """
            rows = await connection.fetch(query)
            return [TradingResult(**row) for row in rows]
        finally:
            await connection.close()
    pass
