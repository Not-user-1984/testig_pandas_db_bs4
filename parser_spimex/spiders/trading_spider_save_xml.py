import scrapy
import pandas as pd
import os
from datetime import datetime
import requests
from scrapy.utils.log import logger


class TradingSpiderSave(scrapy.Spider):
    name = "trading_spider_save"
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
    }

    def start_requests(self):
        """
        Запускает паука. Проверяет CSV-файл и начинает обработку данных.
        """
        csv_file = self.settings.get("CSV_FILE")
        base_save_dir = self.settings.get("BASE_SAVE_DIR")

        self._create_year_folders(base_save_dir)

        if not self._validate_csv_file(csv_file):
            return

        df = pd.read_csv(csv_file, encoding="utf-8")

        for index, row in df.iterrows():
            yield scrapy.Request(
                url="https://example.com",
                callback=self.parse_row,
                meta={"row": row, "base_save_dir": base_save_dir},
                dont_filter=True,
            )

    def parse_row(self, response):
        """
        Обрабатывает одну строку из CSV-файла.
        """
        row = response.meta["row"]
        base_save_dir = response.meta["base_save_dir"]

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
            self._download_xls(url, save_path)
        except ValueError:
            logger.error(f"Не удалось распознать дату: {date}")
        except Exception as e:
            logger.error(f"Ошибка при обработке строки: {e}")

    def _create_year_folders(self, base_dir):
        """
        Создаёт папки для каждого года в указанной базовой директории.
        """
        min_year = self.settings.get("MIN_YEAR")
        for year in range(min_year, datetime.now().year + 1):
            year_folder = os.path.join(base_dir, str(year))
            if not os.path.exists(year_folder):
                os.makedirs(year_folder)
                logger.info(f"Создана папка: {year_folder}")

    def _validate_csv_file(self, csv_file):
        """
        Проверяет, существует ли CSV-файл и содержит ли он необходимые столбцы.
        """
        if not os.path.exists(csv_file):
            logger.error(f"Файл {csv_file} не найден. Убедитесь, что он существует.")
            return False

        try:
            df = pd.read_csv(csv_file, encoding="utf-8")
        except Exception as e:
            logger.error(f"Ошибка при чтении файла {csv_file}: {e}")
            return False

        if "Дата торгов" not in df.columns or "Ссылка на скачивание" not in df.columns:
            logger.error(
                "Файл не содержит необходимых столбцов 'Дата торгов' и 'Ссылка на скачивание'."
            )
            return False

        return True

    def _download_xls(self, url, save_path):
        """
        Скачивает XLS-файл по указанной ссылке и сохраняет его по указанному пути.
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(save_path, "wb") as file:
                for chunk in response.iter_content():
                    file.write(chunk)
            logger.info(f"Файл сохранён: {save_path}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при скачивании файла {url}: {e}")
