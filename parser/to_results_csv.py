import os
import pyexcel as pe
import pandas as pd
from config import URL_SAVE_DIR, XML_SAVE_DIR
from utils import normalize_csv, get_output_path
from logger_config import logger
import time


def _find_header_index(data):
    """
    Ищет индекс строки с заголовком "Единица измерения: Метрическая тонна".
    """
    for i, row in enumerate(data):
        if "Единица измерения: Метрическая тонна" in row:
            return i
    return None


def _parse_xls_file(file_path):
    """
    Парсит XLS-файл и возвращает обработанный DataFrame.
    """
    try:
        data = pe.get_array(file_name=file_path)

        header_index = _find_header_index(data)
        if header_index is None:
            logger.info(
                f"Таблица 'Единица измерения: Метрическая тонна' не найдена в файле: {file_path}"
            )
            return None

        headers = data[header_index + 1]
        df = pd.DataFrame(data[header_index + 2 :], columns=headers)

        df = df.dropna(how="all")
        df = normalize_csv(df)

        if "Количество Договоров, шт." in df.columns:
            try:
                df["Количество Договоров, шт."] = pd.to_numeric(
                    df["Количество Договоров, шт."], errors="coerce"
                )
                df = df[df["Количество Договоров, шт."] > 0]
                df["Количество Договоров, шт."] = df[
                    "Количество Договоров, шт."
                ].astype(int)
            except Exception as e:
                logger.error(
                    f"Ошибка обработки колонки 'Количество Договоров, шт.': {e}"
                )
                return None
        else:
            logger.error("Колонка 'Количество Договоров, шт.' отсутствует в данных.")
            return None

        return df
    except Exception as e:
        logger.error(
            f"Ошибка при обработке файла {file_path}: {e}"
            )
        return None


def _process_data(df, file_path):
    """
    Обрабатывает данные и возвращает результирующий DataFrame.
    """
    date = os.path.splitext(os.path.basename(file_path))[0]

    df.columns = df.columns.str.replace(r"\s+", " ", regex=True).str.strip()

    if "Код Инструмента" not in df.columns:
        logger.error("Столбец 'Код Инструмента' отсутствует!")
        logger.error("Доступные столбцы:", df.columns.tolist())
        return None

    result_df = pd.DataFrame(
        columns=[
            "id",
            "exchange_product_id",
            "exchange_product_name",
            "oil_id",
            "delivery_basis_id",
            "delivery_basis_name",
            "delivery_type_id",
            "volume",
            "total",
            "count",
            "date",
        ]
    )

    for index, row in df.iterrows():
        try:
            exchange_product_id = row["Код Инструмента"]
            exchange_product_name = row["Наименование Инструмента"]
            delivery_basis_name = row["Базис поставки"]
            volume = row["Объем Договоров в единицах измерения"]
            total = row["Обьем Договоров, руб."]
            count = row["Количество Договоров, шт."]

            oil_id = exchange_product_id[:4]
            delivery_basis_id = exchange_product_id[4:7]
            delivery_type_id = exchange_product_id[-1]

            result_df.loc[index] = [
                index + 1,
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
            ]
        except KeyError as e:
            logger.error(f"Ошибка обработки строки {index}: {e}")
            continue

    return result_df


def _parse_all_xls_files(base_dir):
    """
    Парсит все XLS-файлы в указанной директории.
    """
    all_data = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".xls"):
                file_path = os.path.join(root, file)
                logger.info(f"Обрабатывается файл: {file_path}")

                result = _parse_xls_file(file_path)
                if result is not None and not result.empty:
                    processed_data = _process_data(result, file_path)
                    if processed_data is not None:
                        all_data.append(processed_data)

    if len(all_data) > 0:
        final_df = pd.concat(all_data, ignore_index=True)
        return final_df
    else:
        logger.warning("Нет данных для сохранения.")
        return None


def main():
    """
    Основная функция для обработки XLS-файлов.
    """
    start_time = time.time()

    result_df = _parse_all_xls_files(XML_SAVE_DIR)
    if result_df is not None:
        base_path = os.path.abspath(os.path.dirname(__file__))

        output_path = get_output_path(base_path, URL_SAVE_DIR)

        result_df.to_csv(output_path, index=False, encoding="utf-8")
        logger.info(f"Результаты сохранены в файл: {output_path}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time_minutes = elapsed_time / 60
        logger.info(
            f"Парсер завершил работу. Время выполнения: {elapsed_time_minutes:.2f} минут."
            )


if __name__ == "__main__":
    main()
