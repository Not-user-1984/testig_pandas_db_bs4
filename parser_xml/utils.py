import os
import pandas as pd

# from logger_config import logger
# # Настройка логирования


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


def get_absolute_path(base_path, relative_path):
    """
    Формирует абсолютный путь на основе базового пути и относительного пути.
    """
    return os.path.join(base_path, relative_path)


def ensure_directory_exists(path):
    """
    Создает директорию, если она не существует.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        # logger.info(f"Создана директория: {path}")


def get_output_path(base_path, relative_path):
    """
    Формирует абсолютный путь для сохранения файла и проверяет существование директории.
    """
    # Формируем абсолютный путь
    output_path = get_absolute_path(base_path, relative_path)

    # Убеждаемся, что директория существует
    ensure_directory_exists(os.path.dirname(output_path))

    return output_path
