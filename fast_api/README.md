# FastAPI Trading Results Application

Это FastAPI-приложение для работы с данными о результатах торгов из таблицы `spimex_spimextradingresults`. Приложение предоставляет API для получения данных в формате JSON, включая фильтрацию по различным параметрам.

## Видео пример работы

[Видео демонстрация](https://disk.yandex.ru/i/Vq62IFYSuQnd6A)

---

## Структура проекта

```plaintext
fastapi-trading-results/
├── api/                       # Слой API (FastAPI эндпоинты)
│   └── v1/
│       └── endpoints/
│           └── trading.py
├── core/                      # Основные настройки и конфигурации
│   └── config.py
├── database/                  # Слой работы с базой данных
│   ├── models/                # Модели SQLAlchemy
│   │   └── trading.py
│   └── unit_of_work.py        # Паттерн Unit of Work
├── infra/                     # Слой инфраструктуры
│   └── sql/                   # SQL-репозитории
│       └── trading.py
├── repositories/              # Слой репозиториев
│   └── trading.py             # Абстрактный репозиторий и его реализация
├── services/                  # Слой бизнес-логики
│   └── trading.py             # Сервис для работы с торговыми данными
├── schemas/                   # Схемы Pydantic
│   └── trading.py
├── main.py                    # Точка входа в приложение
├── requirements.txt           # Зависимости
└── README.md                  # Документация
```

---

## Основные функции

### 1. Получение списка последних торговых дней
- **Эндпоинт**: `/last_trading_dates/`
- **Параметры**:
  - `limit` (опционально): Количество последних торговых дней (по умолчанию 10).

### 2. Получение динамики торгов за указанный период
- **Эндпоинт**: `/dynamics/`
- **Параметры**:
  - `oil_id` (опционально): Идентификатор нефти.
  - `delivery_type_id` (опционально): Идентификатор типа доставки.
  - `delivery_basis_id` (опционально): Идентификатор базиса доставки.
  - `start_date` (опционально): Начальная дата периода.
  - `end_date` (опционально): Конечная дата периода.
  - `skip` (опционально): Количество записей для пропуска (по умолчанию 0).
  - `limit` (опционально): Количество записей для возврата (по умолчанию 10).

### 3. Получение последних торговых результатов
- **Эндпоинт**: `/trading_results/`
- **Параметры**:
  - `oil_id` (опционально): Идентификатор нефти.
  - `delivery_type_id` (опционально): Идентификатор типа доставки.
  - `delivery_basis_id` (опционально): Идентификатор базиса доставки.
  - `skip` (опционально): Количество записей для пропуска (по умолчанию 0).
  - `limit` (опционально): Количество записей для возврата (по умолчанию 10).

---

## Требования

- Python 3.8+
- PostgreSQL
- Redis (для кэширования)

---

## Установка

### 1. Создайте файл `.env` с содержимым:

```dotenv
# Секретный ключ FastAPI
SECRET_KEY='mySecret'

# Настройки PostgreSQL
POSTGRES_DB=spimex_db
POSTGRES_USER=spimex_user
POSTGRES_PASSWORD=spimex_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Настройки Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Время сброса кэша (опционально)
CACHE_RESET_TIME=14:11
```

### 2. Запустите приложение с помощью Docker Compose

```bash
cd fastapi-trading-results
docker-compose up -d
```

### 3. Импортируйте данные в базу данных

```bash
python parser_xml/asyn_csv.py
```

---

## Документация API

После запуска приложения, документация API будет доступна по следующим адресам:

- **Swagger UI**: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
- **ReDoc**: [http://127.0.0.1:8001/redoc](http://127.0.0.1:8001/redoc)

---

## Примеры запросов

### 1. Получение последних торговых дней

```bash
curl -X 'GET' \
  http://localhost/api/v1/trading/last_trading_dates/ \
  -H 'accept: application/json'
```

### 2. Получение динамики торгов

```bash
curl -X 'GET' \
  http://localhost:8001/api/v1/trading/dynamics/?delivery_basis_id=ANK \
  -H 'accept: application/json'
```

### 3. Получение торговых результатов

```bash
curl -X 'GET' \
  http://localhost:8001/api/v1/trading/trading_results/?skip=20&limit=100 \
  -H 'accept: application/json'
