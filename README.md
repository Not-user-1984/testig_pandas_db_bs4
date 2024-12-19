### README.md

---

# Парсер результатов торгов на SPIMEX

Этот проект представляет собой автоматизированный парсер данных с сайта [SPIMEX](https://spimex.com), который извлекает результаты торгов нефтепродуктами и сохраняет их в удобном формате. Проект состоит из нескольких этапов, каждый из которых выполняет определённую задачу: парсинг ссылок на файлы, скачивание файлов и обработка данных.

---

## Запуск парсера

### Запуск всех этапов:
```bash
python run_parser.py --stage all
```

### Запуск отдельных этапов:
- Парсинг ссылок:
  ```bash
  python run_parser.py --stage parse
  ```
- Скачивание файлов:
  ```bash
  python run_parser.py --stage download
  ```
- Обработка файлов:
  ```bash
  python run_parser.py --stage results
  ```

---

## Структура проекта

Проект организован в виде нескольких модулей, каждый из которых отвечает за определённый этап работы парсера. Вот структура папок и файлов:

```
parser/
├── parse.py                # Парсинг ссылок на XLS-файлы
├── download_xls.py         # Скачивание XLS-файлов
├── to_results_csv.py       # Обработка XLS-файлов и сохранение результатов
├── run_parser.py           # Основной файл запуска этапов
├── logger_config.py        # Конфигурация логирования
├── config.py               # Конфигурация проекта
├── utils.py                # Вспомогательные функции
├── raw/                    # Папка для хранения промежуточных данных
│   └── trading_results.csv # CSV-файл с ссылками на XLS-файлы
├── downloaded_xls_files/   # Папка для хранения скачанных XLS-файлов
└── README.md               # Документация проекта
```

---

## Установка и настройка

1. **Клонируйте репозиторий:**
   ```bash
   git clone git@github.com:Not-user-1984/testig_pandas_db_bs4.git
   cd parser
   ```

2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройте конфигурацию:**
   - Откройте файл `config.py` и убедитесь, что все параметры настроены корректно:
     - `BASE_URL`: URL страницы с результатами торгов.
     - `BASE_DOMAIN`: Базовый домен для ссылок.
     - `MIN_YEAR`: Минимальный год для обработки данных.
     - `URL_SAVE_DIR`: Путь для сохранения конечного результата.

---

## Этапы парсинга

### 1. Парсинг ссылок на XLS-файлы (`parse.py`)

- **Описание:**
  - Парсер извлекает ссылки на XLS-файлы с результатами торгов с сайта SPIMEX.
  - Извлекаются даты торгов и ссылки на файлы.
  - Данные сохраняются в CSV-файл `raw/trading_results.csv`.

- **Сохранение:**
  - Файл: `raw/trading_results.csv`
  - Структура:
    ```
    Дата торгов,Ссылка на скачивание
    12.12.2023,https://spimex.com/file1.xls
    13.12.2023,https://spimex.com/file2.xls
    ```

---

### 2. Скачивание XLS-файлов (`download_xls.py`)

- **Описание:**
  - Скачивает XLS-файлы, указанные в `raw/trading_results.csv`.
  - Файлы сохраняются в папку `downloaded_xls_files`, организованную по годам.

- **Сохранение:**
  - Папка: `downloaded_xls_files/<год>/`
  - Пример:
    ```
    downloaded_xls_files/
    ├── 2023/
    │   ├── 12.12.2023_0.xls
    │   ├── 13.12.2023_1.xls
    ```

---

### 3. Обработка XLS-файлов и сохранение результатов (`to_results_csv.py`)

- **Описание:**
  - Обрабатывает скачанные XLS-файлы.
  - Извлекает данные и сохраняет их в конечный CSV-файл.

- **Сохранение:**
  - Файл: `../app/spimex/migrations/cvs/spimex.cvs`
  - Структура:
    ```
    id,exchange_product_id,exchange_product_name,oil_id,delivery_basis_id,delivery_basis_name,delivery_type_id,volume,total,count,date,created_on,updated_on
    1,A100ANK060F,"Бензин (АИ-100-К5), Ангарск-группа станций",A100,ANK,Ангарск-группа станций,F,60,5304000,1,12.12.2024_0,2024-12-19 10:30:30.249680,2024-12-19 10:30:30.249686
    ```

---

## Административная панель Django

После загрузки данных в базу данных через парсер, вы можете использовать административную панель Django для управления данными.

### Настройка административной панели

1. **Примените миграции:**
   ```bash
   python manage.py migrate
   ```

2. **Создайте суперпользователя:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Загрузите данные в базу:**
   ```bash
   python manage.py load_data spimex/migrations/cvs/spimex.cvs # путь до файла можно менять
   ```

4. **Запустите сервер:**
   ```bash
   python manage.py runserver
   ```

5. **Откройте административную панель:**
   Перейдите по адресу [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) и войдите с использованием созданного суперпользователя.

---

### Возможности административной панели

В административной панели доступны следующие функции:

#### Отображение данных:
- **Поля:**
  - `exchange_product_id`
  - `exchange_product_name`
  - `oil_id`
  - `delivery_basis_id`
  - `delivery_basis_name`
  - `delivery_type_id`
  - `volume`
  - `total`
  - `count`
  - `date`
  - `created_on`
  - `updated_on`

#### Поиск:
- Поиск по следующим полям:
  - `exchange_product_id`
  - `exchange_product_name`
  - `oil_id`
  - `delivery_basis_id`
  - `delivery_basis_name`
  - `delivery_type_id`
  - `volume`
  - `total`
  - `count`
  - `date`

#### Фильтрация:
- Фильтрация по следующим полям:
  - `exchange_product_id`
  - `oil_id`
  - `delivery_basis_id`
  - `delivery_type_id`
  - `date`
  - `created_on`
  - `updated_on`

#### Редактирование:
- Редактируемые поля:
  - `volume`
  - `total`
  - `count`

#### Сортировка:
- Сортировка по убыванию даты (`-date`) и по возрастанию `exchange_product_id`.

---

## Требования

- Python 3.8+
- Библиотеки: `requests`, `beautifulsoup4`, `pandas`, `pyexcel` `django`


---

## Лицензия

MIT License
