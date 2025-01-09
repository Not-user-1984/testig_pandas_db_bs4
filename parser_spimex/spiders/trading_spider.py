import scrapy
from bs4 import BeautifulSoup
import pandas as pd
import os
from parser_spimex.logger_config import logger


class TradingSpider(scrapy.Spider):
    name = "trading_spider"

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
    }

    def start_requests(self):
        base_url = self.settings.get("BASE_URL")
        yield scrapy.Request(url=base_url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        xls_links, dates = self._extract_xls_links_and_dates(soup)

        for date in dates:
            if date and not self._validate_date(date):
                return

        self._save_to_csv(dates, xls_links)

        next_page_url = self._get_next_page_url(soup)
        if next_page_url:
            base_domain = self.settings.get("BASE_DOMAIN")
            yield response.follow(base_domain + next_page_url, self.parse)

    def _extract_xls_links_and_dates(self, soup):
        xls_links = []
        dates = []

        for item in soup.find_all("div", class_="accordeon-inner__item"):
            link_element = item.find("a", class_="accordeon-inner__item-title link xls")
            if link_element:
                xls_links.append(link_element["href"])
            else:
                xls_links.append(None)
            date_element = soup.select_one(
                "html body main section div div:nth-of-type(2) div div div:nth-of-type(2) div:nth-of-type(1) div div:nth-of-type(1) div:nth-of-type(5) div div:nth-of-type(2) div p span"
            )
            if date_element:
                date = date_element.text.strip()
                dates.append(date)
            else:
                dates.append(None)

        return xls_links, dates

    def _get_next_page_url(self, soup):
        next_page_link = soup.find("li", class_="bx-pag-next")
        if next_page_link and next_page_link.find("a"):
            return next_page_link.find("a")["href"]
        return None

    def _validate_date(self, date):
        min_year = self.settings.get("MIN_YEAR")
        date_parts = date.split(".")
        if len(date_parts) >= 3:
            year = int(date_parts[-1])
            if year < min_year:
                logger.warning(
                    f"Дата торгов {date} меньше {min_year} года. Остановка парсинга."
                )
                return False
        else:
            logger.warning(f"Некорректный формат даты: {date}")
            return False
        return True

    def _save_to_csv(self, dates, xls_links):
        base_domain = self.settings.get("BASE_DOMAIN")
        csv_file = self.settings.get("CSV_FILE")

        data = {
            "Дата торгов": dates,
            "Ссылка на скачивание": [
                base_domain + link if link else None for link in xls_links
            ],
        }
        df = pd.DataFrame(data)

        df = df[df["Дата торгов"].notna() & df["Ссылка на скачивание"].notna()]

        if os.path.exists(csv_file):
            df.to_csv(
                csv_file,
                mode="a", header=False, index=False, encoding="utf-8")
        else:
            df.to_csv(csv_file, index=False, encoding="utf-8")

        logger.info(f"Данные сохранены в файл: {csv_file}")
