from datetime import date, datetime
from typing import List, Optional
import asyncpg

from schemas.trading import TradingResult
from repositories.base import BaseRepository  # Импортируем интерфейс


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


class TradingRepositoryImpl(BaseRepository):  # Реализуем интерфейс BaseRepository
    async def get_last_trading_dates(self, limit: int = 10) -> List[date]:
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
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[TradingResult]:
        """
        Возвращает динамику торгов за указанный период.
        """
        connection = await get_db_connection()
        try:
            query = """
                SELECT exchange_product_id, exchange_product_name, oil_id, delivery_basis_id, delivery_basis_name,
                    delivery_type_id, volume, total, count, date, created_on, updated_on
                FROM spimex_spimextradingresults
                WHERE ($1::text IS NULL OR oil_id = $1)
                AND ($2::text IS NULL OR delivery_type_id = $2)
                AND ($3::text IS NULL OR delivery_basis_id = $3)
                AND ($4::date IS NULL OR date >= $4)
                AND ($5::date IS NULL OR date <= $5)
                ORDER BY date
                OFFSET $6
                LIMIT $7;
            """
            rows = await connection.fetch(
                query, oil_id, delivery_type_id, delivery_basis_id, start_date, end_date, skip, limit
            )
            print("Rows from DB:", rows)
            return [TradingResult(**row) for row in rows]
        finally:
            await connection.close()

    async def get_trading_results(
        self,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[TradingResult]:
        """
        Возвращает результаты торгов для указанных параметров.
        """
        connection = await get_db_connection()
        try:
            query = """
                SELECT exchange_product_id, exchange_product_name, oil_id, delivery_basis_id, delivery_basis_name,
                    delivery_type_id, volume, total, count, date, created_on, updated_on
                FROM spimex_spimextradingresults
                WHERE ($1::text IS NULL OR oil_id = $1)
                AND ($2::text IS NULL OR delivery_type_id = $2)
                AND ($3::text IS NULL OR delivery_basis_id = $3)
                ORDER BY date DESC
                OFFSET $4
                LIMIT $5;
            """
            rows = await connection.fetch(
                query, oil_id, delivery_type_id, delivery_basis_id, skip, limit
            )
            return [TradingResult(**row) for row in rows]
        finally:
            await connection.close()

    async def get_total_count(
        self,
        oil_id: Optional[str] = None,
        delivery_type_id: Optional[str] = None,
        delivery_basis_id: Optional[str] = None,
    ) -> int:
        """
        Возвращает общее количество записей, соответствующих фильтрам.
        """
        connection = await get_db_connection()
        try:
            query = """
                SELECT COUNT(*)
                FROM spimex_spimextradingresults
                WHERE ($1::text IS NULL OR oil_id = $1)
                  AND ($2::text IS NULL OR delivery_type_id = $2)
                  AND ($3::text IS NULL OR delivery_basis_id = $3);
            """
            result = await connection.fetchval(query, oil_id, delivery_type_id, delivery_basis_id)
            return result
        finally:
            await connection.close()