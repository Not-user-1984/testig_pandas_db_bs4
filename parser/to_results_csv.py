import os
import pyexcel as pe
import pandas as pd
from datetime import datetime



def normalize_csv(df):
    """
    Нормализует DataFrame:
    - Удаляет лишние запятые и пробелы.
    - Убирает пустые строки и столбцы.
    """
    df.columns = (
        df.columns
        .str.replace(r'\s+', ' ', regex=True)
        .str.replace(r',+', ',', regex=True)
        .str.strip()
    )

    df = df.dropna(how="all").dropna(axis=1, how="all")
    return df


def parse_xls_file(file_path):
    """
    Парсит XLS-файл, обрабатывает данные и сохраняет DataFrame в файл.
    """
    try:
        # Считываем данные из файла
        data = pe.get_array(file_name=file_path)

        # Ищем строку "Единица измерения: Метрическая тонна"
        header_index = None
        for i, row in enumerate(data):
            if "Единица измерения: Метрическая тонна" in row:
                header_index = i
                break

        if header_index is None:
            print(f"Таблица 'Единица измерения: Метрическая тонна' не найдена в файле: {file_path}")
            return None

        # Используем следующую строку как заголовки таблицы
        headers = data[header_index + 1]
        df = pd.DataFrame(data[header_index + 2:], columns=headers)

        # Удаляем пустые строки
        df = df.dropna(how="all")
        df = normalize_csv(df)
        print(df)

        # Проверяем колонку "Количество Договоров, шт."
        if "Количество Договоров, шт." in df.columns:
            try:
                df["Количество Договоров, шт."] = pd.to_numeric(
                    df["Количество Договоров, шт."], errors="coerce"
                    )
                df = df[df["Количество Договоров, шт."] > 0]
                df["Количество Договоров, шт."] = df["Количество Договоров, шт."].astype(int)
            except Exception as e:
                print(f"Ошибка обработки колонки 'Количество Договоров, шт.': {e}")
                return None
        else:
            print("Колонка 'Количество Договоров, шт.' отсутствует в данных.")
            return None

        # # Сохраняем DataFrame
        # base_name = os.path.splitext(os.path.basename(file_path))[0]
        # output_file = f"{base_name}_cleaned.csv"
        # df.to_csv(output_file, index=False, encoding="utf-8")
        # print(f"Обработанные данные сохранены в файл: {output_file}")

        return df
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")
        return None



def process_data(df, file_path):
    # Извлекаем дату из имени файла
    date = os.path.splitext(os.path.basename(file_path))[0]

    # Очистка и унификация названий столбцов
    df.columns = df.columns.str.replace(r'\s+', ' ', regex=True).str.strip()

    if "Код Инструмента" not in df.columns:
        print("Столбец 'Код Инструмента' отсутствует!")
        print("Доступные столбцы:", df.columns.tolist())
        return None

    # Создаём новый DataFrame
    result_df = pd.DataFrame(columns=[
        "id", "exchange_product_id", "exchange_product_name", "oil_id",
        "delivery_basis_id", "delivery_basis_name", "delivery_type_id",
        "volume", "total", "count", "date", "created_on", "updated_on"
    ])

    # Обрабатываем каждую строку
    for index, row in df.iterrows():
        try:
            exchange_product_id = row["Код Инструмента"]
            exchange_product_name = row["Наименование Инструмента"]
            delivery_basis_name = row["Базис поставки"]
            volume = row["Объем Договоров в единицах измерения"]
            total = row["Обьем Договоров, руб."]
            count = row["Количество Договоров, шт."]

            # Извлекаем дополнительные поля
            oil_id = exchange_product_id[:4]
            delivery_basis_id = exchange_product_id[4:7]
            delivery_type_id = exchange_product_id[-1]
            # Извлекаем дату из строки

            # date_str = row["Дата торгов"].split('_')[0]  # Берем только "12.12.2024"
            # date = datetime.strptime(date_str, '%d.%m.%Y').date()

            # Добавляем строку в результат
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
                datetime.now(),  # created_on
                datetime.now()   # updated_on
            ]
        except KeyError as e:
            print(f"Ошибка обработки строки {index}: {e}")
            continue

    return result_df


def parse_all_xls_files(base_dir):
    all_data = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".xls"):  # Обрабатываем только .xls файлы
                file_path = os.path.join(root, file)
                print(f"Обрабатывается файл: {file_path}")

                # Парсим файл
                result = parse_xls_file(file_path)
                if result is not None and not result.empty:
                    processed_data = process_data(result, file_path)
                    if processed_data is not None:
                        all_data.append(processed_data)

    # Объединяем все результаты в один DataFrame
    if len(all_data) > 0:
        final_df = pd.concat(all_data, ignore_index=True)
        return final_df
    else:
        print("Нет данных для сохранения.")
        return None


def main():
    # Базовая директория с XLS-файлами
    base_dir = "downloaded_xls_files"
    # base_dir = "test"
    # Парсим все XLS-файлы
    result_df = parse_all_xls_files(base_dir)

    if result_df is not None:
        # Сохраняем результаты в CSV-файл
        result_df.to_csv("app/spimex/migrations/cvs/spimex_trading_results.csv", index=False, encoding="utf-8")
        print("Результаты сохранены в файл: spimex_trading_results.csv")

if __name__ == "__main__":
    main()