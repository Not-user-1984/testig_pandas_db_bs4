import os
import pyexcel as pe
import pandas as pd
from scrapy import Spider, Request
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import logger
from ..items import ParsedDataItem

class XlsParserSpider(Spider):
    name = "results_xls_spider"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        settings = get_project_settings()
        self.xml_save_dir = settings.get("XML_SAVE_DIR")

    def start_requests(self):
        """Генерация начальных запросов."""
        for root, dirs, files in os.walk(self.xml_save_dir):
            for file in files:
                if file.endswith(".xls"):
                    file_path = os.path.join(root, file)
                    logger.info(f"Обрабатывается файл: {file_path}")
                    yield Request(
                        url="https://example.com",
                        meta={"file_path": file_path},
                        dont_filter=True,
                    )

    def parse_xls_file(self, response):
        """Парсит XLS-файл и возвращает данные."""
        file_path = response.meta["file_path"]

        try:
            # Чтение и парсинг XLS-файла
            data = pe.get_array(file_name=file_path)

            header_index = self._find_header_index(data)
            if header_index is None:
                logger.info(
                    f"Таблица 'Единица измерения: Метрическая тонна' не найдена в файле: {file_path}"
                )
                return

            headers = data[header_index + 1]
            df = pd.DataFrame(data[header_index + 2:], columns=headers)

            df = df.dropna(how="all")
            df = self._normalize_csv(df)

            if "Количество Договоров, шт." in df.columns:
                try:
                    df["Количество Договоров, шт."] = pd.to_numeric(df["Количество Договоров, шт."], errors="coerce")
                    df = df[df["Количество Договоров, шт."] > 0]
                    df["Количество Договоров, шт."] = df["Количество Договоров, шт."].astype(int)
                except Exception as e:
                    logger.error(f"Ошибка обработки колонки 'Количество Договоров, шт.': {e}")
                    return
            else:
                logger.error("Колонка 'Количество Договоров, шт.' отсутствует в данных.")
                return

            logger.info(f"Обработан файл: {file_path}")
            logger.info(f"Найдено строк: {len(df)}")

            yield from self._process_data(df, file_path)

        except Exception as e:
            logger.error(f"Ошибка при обработке файла {file_path}: {e}")

    def _find_header_index(self, data):
        """Ищет индекс строки с заголовком 'Единица измерения: Метрическая тонна'."""
        for i, row in enumerate(data):
            if "Единица измерения: Метрическая тонна" in row:
                return i
        return None

    def _normalize_csv(self, df):
        """Нормализует DataFrame."""
        df.columns = df.columns.str.strip()
        df = df.dropna(how="all")
        return df

    def _process_data(self, df, file_path):
        """Обрабатывает данные и возвращает результирующий DataFrame."""
        date = os.path.splitext(os.path.basename(file_path))[0]

        df.columns = df.columns.str.replace(r"\s+", " ", regex=True).str.strip()

        if "Код Инструмента" not in df.columns:
            logger.error("Столбец 'Код Инструмента' отсутствует!")
            logger.error("Доступные столбцы:", df.columns.tolist())
            return

        for index, row in df.iterrows():
            try:
                item = ParsedDataItem()
                item["id"] = index + 1
                item["exchange_product_id"] = row["Код Инструмента"]
                item["exchange_product_name"] = row["Наименование Инструмента"]
                item["delivery_basis_name"] = row["Базис поставки"]
                item["volume"] = row["Объем Договоров в единицах измерения"]
                item["total"] = row["Обьем Договоров, руб."]
                item["count"] = row["Количество Договоров, шт."]
                item["oil_id"] = row["Код Инструмента"][:4]
                item["delivery_basis_id"] = row["Код Инструмента"][4:7]
                item["delivery_type_id"] = row["Код Инструмента"][-1]
                item["date"] = date

                yield item
            except KeyError as e:
                logger.error(f"Ошибка обработки строки {index}: {e}")
                continue
