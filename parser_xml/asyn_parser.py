import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
from logger_config import logger
from config import BASE_URL, BASE_DOMAIN, MIN_YEAR


async def _extract_xls_links_and_dates(soup):
    """
    Извлекает все ссылки на XLS-файлы и даты торгов с текущей страницы.
    """
    xls_links = []
    dates = []

    for item in soup.find_all("div", class_="accordeon-inner__item"):
        link_element = item.find(
            "a", class_="accordeon-inner__item-title link xls"
            )
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


async def _get_next_page_url(soup):
    """
    Извлекает ссылку на следующую страницу из пагинации.
    """
    next_page_link = soup.find("li", class_="bx-pag-next")
    if next_page_link and next_page_link.find("a"):
        return next_page_link.find("a")["href"]
    return None


async def _validate_date(date):
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


async def _save_to_csv(dates, xls_links):
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
            mode="a",
            header=False,
            index=False,
            encoding="utf-8")
    else:
        df.to_csv(file_path, index=False, encoding="utf-8")

    logger.info(f"Данные сохранены в файл: {file_path}")


async def _ensure_raw_folder_exists():
    """
    Проверяет и создает папку 'raw', если её нет.
    """
    if not os.path.exists("raw"):
        os.makedirs("raw")
        logger.info("Папка 'raw' создана.")


async def _download_file(session, url, semaphore):
    """
    Скачивает один файл с ограничением количества одновременных запросов.
    """
    async with semaphore:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                logger.info(f"Скачан файл: {url}")
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при скачивании файла {url}: {e}")


async def _process_page(session, page_url, semaphore):
    """
    Обрабатывает одну страницу, извлекает данные и сохраняет их.
    """
    logger.info(f"Обрабатывается страница: {page_url}")
    try:
        async with session.get(page_url) as response:
            response.raise_for_status()
            html = await response.text()
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при загрузке страницы {page_url}: {e}")
        return None

    soup = BeautifulSoup(html, "html.parser")
    xls_links, dates = await _extract_xls_links_and_dates(soup)

    for date in dates:
        if date and not await _validate_date(date):
            return None

    await _save_to_csv(dates, xls_links)

    download_tasks = [
        _download_file(session, BASE_DOMAIN + link, semaphore)
        for link in xls_links
        if link
    ]
    await asyncio.gather(*download_tasks)


async def main(max_pages=10):
    await _ensure_raw_folder_exists()

    start_time = time.time()
    logger.info("Начало парсинга...")

    page_urls = [BASE_URL]
    print(page_urls)
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        while len(page_urls) < max_pages:
            current_url = page_urls[-1]
            logger.info(f"Загружается страница: {current_url}")
            try:
                async with session.get(current_url) as response:
                    response.raise_for_status()
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    next_page_url = await _get_next_page_url(soup)
                    if next_page_url:
                        page_urls.append(BASE_DOMAIN + next_page_url)
                    else:
                        break
            except aiohttp.ClientError as e:
                logger.error(
                    f"Ошибка при загрузке страницы {current_url}: {e}"
                    )
                break

    logger.info(f"Сформировано {len(page_urls)} ссылок на страницы.")

    download_semaphore = asyncio.Semaphore(1)

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        tasks = [_process_page(
            session, url, download_semaphore) for url in page_urls]
        await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(
        f"Парсинг завершён. Время выполнения: {elapsed_time:.2f} секунд."
        )


if __name__ == "__main__":
    asyncio.run(main(max_pages=10))
