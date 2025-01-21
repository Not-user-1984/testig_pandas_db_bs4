

# Тесты для модуля торговых данных

Этот проект содержит тесты для модуля, который работает с торговыми данными. Тесты написаны с использованием `pytest` и `pytest-asyncio` для асинхронных операций.

## Видео
```
https://disk.yandex.ru/i/k-sqhlvcHxTQ9A
```

## Структура проекта

```
fast_api/tests/
├── conftest.py                # Основные фикстуры для всех тестов
├── trading/
│   ├── conftest.py            # Фикстуры для тестов торговых данных
│   ├── test_data.py           # Тестовые данные и параметры для тестов
│   └── test_trading_results.py # Тесты для торговых данных
```

## Зависимости

Для запуска тестов убедитесь, что у вас установлены следующие зависимости:

- `pytest`
- `pytest-asyncio`
- `sqlalchemy`
- `asyncpg` (или другой асинхронный драйвер для базы данных)

Установите зависимости с помощью команды:

```bash
pip install pytest pytest-asyncio sqlalchemy asyncpg
```

## Запуск тестов

Для запуска тестов выполните следующую команду:

```bash
pytest fast_api/tests/
```

Если вы используете `Makefile`, вы можете запустить тесты через Docker:

```bash
make tests
```

## Описание тестов

### 1. **Тесты для получения последних торговых дат**

- **Файл:** `test_trading_results.py`
- **Тест:** `test_get_last_trading_dates`
- **Описание:** Проверяет, что метод `get_last_trading_dates` возвращает корректные даты и их количество не превышает указанный лимит.
- **Параметры:**
  - `expected_trading_dates`: Ожидаемый список дат.

### 2. **Тесты для получения результатов торгов**

- **Файл:** `test_trading_results.py`
- **Тест:** `test_get_trading_results`
- **Описание:** Проверяет, что метод `get_trading_results` возвращает результаты, соответствующие заданным параметрам (например, `oil_id`, `delivery_type_id`, `delivery_basis_id`).
- **Параметры:**
  - `trading_results_test_case`: Тестовые данные и ожидаемые условия.

### 3. **Тесты для получения динамики торгов**

- **Файл:** `test_trading_results.py`
- **Тест:** `test_get_dynamics`
- **Описание:** Проверяет, что метод `get_dynamics` возвращает данные, соответствующие заданным параметрам (например, `start_date`, `end_date`, `oil_id`).
- **Параметры:**
  - `dynamics_test_case`: Тестовые данные и ожидаемые условия.

### 4. **Тесты для получения общего количества записей**

- **Файл:** `test_trading_results.py`
- **Тест:** `test_get_total_count`
- **Описание:** Проверяет, что метод `get_total_count` возвращает корректное количество записей для заданных параметров.
- **Параметры:**
  - `oil_id`, `delivery_type_id`, `delivery_basis_id`: Параметры фильтрации.

## Фикстуры

### 1. **Фикстура `session`**

- **Файл:** `conftest.py`
- **Описание:** Создает асинхронную сессию для работы с базой данных.
- **Используется в:** Всех тестах, которые взаимодействуют с базой данных.

### 2. **Фикстура `dynamics_test_case`**

- **Файл:** `test_data.py`
- **Описание:** Предоставляет тестовые данные для проверки динамики торгов.
- **Используется в:** `test_get_dynamics`.

### 3. **Фикстура `trading_results_test_case`**

- **Файл:** `test_data.py`
- **Описание:** Предоставляет тестовые данные для проверки результатов торгов.
- **Используется в:** `test_get_trading_results`.

### 4. **Фикстура `expected_trading_dates`**

- **Файл:** `test_data.py`
- **Описание:** Предоставляет ожидаемые даты для проверки метода `get_last_trading_dates`.
- **Используется в:** `test_get_last_trading_dates`.

## Тестовые данные

Тестовые данные находятся в файле `test_data.py`. Они включают:

- `test_cases`: Параметры и ожидаемые результаты для тестов динамики торгов.
- `test_cases_trading_results`: Параметры и ожидаемые результаты для тестов результатов торгов.
- `expected_dates`: Ожидаемые даты для тестов последних торговых дат.

## Примеры тестовых данных

### Пример 1: Динамика торгов

```python
{
    "params": {"oil_id": "A100"},
    "expected": lambda results: all(result.oil_id == "A100" for result in results),
}
```

### Пример 2: Результаты торгов

```python
{
    "params": {"oil_id": "A100", "delivery_type_id": "F", "delivery_basis_id": "ANK"},
    "expected": lambda results: (
        all(result.oil_id == "A100" for result in results)
        and all(result.delivery_type_id == "F" for result in results)
        and all(result.delivery_basis_id == "ANK" for result in results)
    ),
}
```

## Логирование

Тесты настроены на вывод логов SQL-запросов (`echo=True` в фикстуре `session`). Это помогает в отладке и проверке корректности запросов.
