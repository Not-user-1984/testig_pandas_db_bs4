import pandas as pd
import requests
import os
from datetime import datetime

from logger_config import logger
from config import MIN_YEAR


def download_xls(url, save_path):
    """
    Скачивает XLS-файл по указанной ссылке и сохраняет его по указанному пути.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content():
                file.write(chunk)
        logger.info(f"Файл сохранён: {save_path}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при скачивании файла {url}: {e}")


def create_year_folders(base_dir):
    """
    Создаёт папки для каждого года в указанной базовой директории.
    """
    for year in range(MIN_YEAR, datetime.now().year + 1):
        year_folder = os.path.join(base_dir, str(year))
        if not os.path.exists(year_folder):
            os.makedirs(year_folder)
            logger.info(f"Создана папка: {year_folder}")


def validate_csv_file(csv_file):
    """
    Проверяет, существует ли CSV-файл и содержит ли он необходимые столбцы.
    """
    if not os.path.exists(csv_file):
        logger.error(
            f"Файл {csv_file} не найден. Убедитесь, что он существует.")
        return False

    try:
        df = pd.read_csv(csv_file, encoding="utf-8")
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {csv_file}: {e}")
        return False

    if "Дата торгов" not in df.columns or "Ссылка на скачивание" not in df.columns:
        logger.error("Файл не содержит необходимых столбцов 'Дата торгов' и 'Ссылка на скачивание'.")
        return False

    return True


def process_row(row, base_save_dir):
    """
    Обрабатывает одну строку из CSV-файла, скачивает файл и сохраняет его.
    """
    date = row["Дата торгов"]
    url = row["Ссылка на скачивание"]

    if pd.isna(date) or pd.isna(url):
        logger.warning(f"Пропущена строка: отсутствует дата или ссылка.")
        return

    try:
        date_obj = datetime.strptime(date, "%d.%m.%Y")
        year = date_obj.year

        file_name = f"{date_obj.strftime('%d.%m.%Y')}_{row.name}.xls"
        save_path = os.path.join(base_save_dir, str(year), file_name)
        logger.info(f"Скачиваем файл: {url}")
        download_xls(url, save_path)
    except ValueError:
        logger.error(f"Не удалось распознать дату: {date}")
    except Exception as e:
        logger.error(f"Ошибка при обработке строки: {e}")


def download_xls_files():
    csv_file = "raw/trading_results.csv"
    base_save_dir = "downloaded_xls_files"

    create_year_folders(base_save_dir)

    if not validate_csv_file(csv_file):
        return

    df = pd.read_csv(csv_file, encoding="utf-8")

    for index, row in df.iterrows():
        process_row(row, base_save_dir)


if __name__ == "__main__":
    download_xls_files()