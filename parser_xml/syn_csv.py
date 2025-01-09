import csv
import time
from datetime import datetime
from typing import List
import psycopg2

DB_CONFIG = {
    "user": "spimex_user",
    "password": "spimex_password",
    "database": "spimex_db",
    "host": "localhost",
    "port": 5432,
}

CSV_FILE_PATH = "parser_xml/results_csv/spimex.cvs"

BATCH_SIZE = 100


def connect_to_db():
    """Создает подключение к базе данных."""
    return psycopg2.connect(**DB_CONFIG)


def ensure_table_exists(connection):
    """Проверяет, существует ли таблица spimex_spimextradingresults, и создает её, если нет."""
    with connection.cursor() as cursor:
        cursor.execute(
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
        connection.commit()


def insert_data(connection, data: List[dict]):
    """Вставляет данные в таблицу spimex_spimextradingresults."""
    with connection.cursor() as cursor:
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
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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

        cursor.executemany(query, rows_to_insert)
        connection.commit()


def process_csv_file(connection):
    """Обрабатывает CSV-файл и загружает данные в базу данных."""
    with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
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
                insert_data(connection, batch)
                batch = []
        if batch:
            insert_data(connection, batch)


def main():
    """Основная функция для запуска скрипта."""
    start_time = time.time()
    connection = connect_to_db()
    try:
        ensure_table_exists(connection)
        process_csv_file(connection)
        print("Data loaded successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
