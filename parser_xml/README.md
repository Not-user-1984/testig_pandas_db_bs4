# Загрузка данных из CSV в PostgreSQL

Этот проект содержит скрипты для загрузки данных из CSV-файла в базу данных PostgreSQL. Включает асинхронную и синхронную версии

---

## Структура проекта

- **[`parser_xml/asyn_csv.py`](parser_xml/asyn_csv.py)**: Асинхронная версия скрипта для загрузки данных.
- **[`sync_csv.py`](parser_xml/syn_csv.py)**: Синхронная версия скрипта для загрузки данных.

## Видео

```
https://disk.yandex.ru/i/MItXWVJnpCX_pg
```

## Требования

- Python 3.11 или выше.
- Установленные зависимости:
  - `asyncpg` для асинхронной работы с PostgreSQL.
  - `aiofiles` для асинхронного чтения файлов.
  - `psycopg2` для синхронной работы с PostgreSQL.

Установите зависимости с помощью команды:

```bash
pip install asyncpg aiofiles psycopg2

cd parser_xml

python sync_cvs.py

python async_csv.py

```
