import asyncio
import asyncpg
import aiofiles
import csv
from datetime import datetime
from typing import List


DB_CONFIG = {
    "user": "spimex_user",
    "password": "spimex_password",
    "database": "spimex_db",
    "host": "localhost",
    "port": 5432,
}


CSV_FILE_PATH = "parser_xml/results_csv/spimex.cvs"

BATCH_SIZE = 100


async def connect_to_db():
    """Создает пул подключений к базе данных."""
    return await asyncpg.create_pool(**DB_CONFIG)


async def ensure_table_exists(pool):
    """Проверяет, существует ли таблица, и создает её, если нет."""
    async with pool.acquire() as connection:
        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS spimex_spimextradingresults (
                exchange_product_id TEXT,
                exchange_product_name TEXT,
                oil_id TEXT,
                delivery_basis_id TEXT,
                delivery_basis_name TEXT,
                delivery_type_id TEXT,
                volume INTEGER,
                total INTEGER,
                count INTEGER,
                date DATE,
                created_on TIMESTAMP,
                updated_on TIMESTAMP
            );
        """
        )


async def insert_data(pool, data: List[dict]):
    """Вставляет данные в таблицу spimex_trading_results."""
    async with pool.acquire() as connection:
        async with connection.transaction():
            query = """
            INSERT INTO spimex_spimextradingresults (
                exchange_product_id,
                exchange_product_name,
                oil_id,
                delivery_basis_id,
                delivery_basis_name,
                delivery_type_id,
                volume,
                total,
                count,
                date,
                created_on,
                updated_on
            ) VALUES (
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12
            )
            """
            now = datetime.now()
            rows_to_insert = []
            for row in data:
                try:
                    date_str = row["date"].split("_")[0]
                    date = datetime.strptime(date_str, "%d.%m.%Y").date()
                    rows_to_insert.append(
                        (
                            row["exchange_product_id"],
                            row["exchange_product_name"],
                            row["oil_id"],
                            row["delivery_basis_id"],
                            row["delivery_basis_name"],
                            row["delivery_type_id"],
                            int(row["volume"]) if row["volume"] else 0,
                            int(row["total"]) if row["total"] else 0,
                            int(row["count"]) if row["count"] else 0,
                            date,
                            now,
                            now,
                        )
                    )
                except (ValueError, KeyError) as e:
                    print(f"Skipping row due to error: {e}")
                    continue

            await connection.executemany(query, rows_to_insert)


async def process_csv_file(pool):
    """Обрабатывает CSV-файл и загружает данные в базу данных."""
    async with aiofiles.open(CSV_FILE_PATH, mode="r", encoding="utf-8") as file:
        content = await file.read()
        lines = content.splitlines()
        reader = csv.DictReader(lines)

        batch = []
        for row in reader:
            if not all(
                row.get(key)
                for key in ["exchange_product_id", "exchange_product_name", "oil_id"]
            ):
                print(f"Skipping row with missing data: {row}")
                continue
            batch.append(row)
            if len(batch) >= BATCH_SIZE:
                await insert_data(pool, batch)
                batch = []
        if batch:
            await insert_data(pool, batch)


async def main():
    """Основная функция для запуска скрипта."""
    start_time = asyncio.get_event_loop().time()
    pool = await connect_to_db()
    try:
        await ensure_table_exists(pool)
        await process_csv_file(pool)
        print("Data loaded successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await pool.close()
    end_time = asyncio.get_event_loop().time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
