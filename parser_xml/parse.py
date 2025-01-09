import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
from logger_config import logger
from config import BASE_URL, BASE_DOMAIN, MIN_YEAR


def _extract_xls_links_and_dates(soup):
    """
    Извлекает все ссылки на XLS-файлы и даты торгов с текущей страницы.
    """
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


def _get_next_page_url(soup):
    """
    Извлекает ссылку на следующую страницу из пагинации.
    """
    next_page_link = soup.find("li", class_="bx-pag-next")
    if next_page_link and next_page_link.find("a"):
        return next_page_link.find("a")["href"]
    return None


def _validate_date(date):
    """
    Проверяет, что дата соответствует минимальному году.
    """
    date_parts = date.split(".")
    if len(date_parts) >= 3:
        year = int(date_parts[-1])
        if year < MIN_YEAR:
            logger.warning(
                f"Дата торгов {date} меньше {MIN_YEAR} года. Остановка парсинга."
            )
            return False
    else:
        logger.warning(f"Некорректный формат даты: {date}")
        return False
    return True


def _save_to_csv(dates, xls_links):
    """
    Сохраняет данные в CSV-файл, добавляя новые данные в существующий файл.
    """
    data = {
        "Дата торгов": dates,
        "Ссылка на скачивание": [
            BASE_DOMAIN + link if link else None for link in xls_links
        ],
    }
    df = pd.DataFrame(data)

    df = df[df["Дата торгов"].notna() & df["Ссылка на скачивание"].notna()]

    file_path = "raw/trading_results.csv"
    if os.path.exists(file_path):
        df.to_csv(
            file_path,
            mode="a", header=False, index=False, encoding="utf-8")
    else:
        df.to_csv(file_path, index=False, encoding="utf-8")

    logger.info(f"Данные сохранены в файл: {file_path}")


def _ensure_raw_folder_exists():
    """
    Проверяет и создает папку 'raw', если её нет.
    """
    if not os.path.exists("raw"):
        os.makedirs("raw")
        logger.info("Папка 'raw' создана.")


def _process_page(page_url, page_counter):
    """
    Обрабатывает одну страницу, извлекает данные и сохраняет их.
    """
    logger.info(f"Обрабатывается страница {page_counter}...")

    try:
        response = requests.get(page_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при загрузке страницы {page_url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    xls_links, dates = _extract_xls_links_and_dates(soup)

    for date in dates:
        if date and not _validate_date(date):
            return None

    _save_to_csv(dates, xls_links)
    return _get_next_page_url(soup)


def main():
    _ensure_raw_folder_exists()

    start_time = time.time()
    logger.info("Начало парсинга...")

    page_url = BASE_URL
    page_counter = 1
    total_files = 0

    while page_url:
        next_page_url = _process_page(page_url, page_counter)
        if next_page_url:
            page_url = BASE_DOMAIN + next_page_url
            page_counter += 1
            total_files += len(
                _extract_xls_links_and_dates(
                    BeautifulSoup
                    (requests.get(page_url).text, "html.parser"))[0]
                    )
            time.sleep(2)
        else:
            logger.info("Достигнута последняя страница.")
            break

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(
        f"Парсинг завершён. Время выполнения: {elapsed_time:.2f} секунд.")
    logger.info(f"Всего скачано файлов: {total_files}")


if __name__ == "__main__":
    main()
