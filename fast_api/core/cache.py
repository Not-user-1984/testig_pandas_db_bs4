from datetime import date, datetime
from functools import wraps
import logging
from typing import Any, Callable, Coroutine
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from aiocache import Cache, cached
from core.config import settings
from aiocache.serializers import PickleSerializer

cache = Cache(
    Cache.REDIS, endpoint="localhost", port=6379, serializer=PickleSerializer()
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def cache_response(expire: int = 60 * 60):
    """
    Декоратор для кэширования ответов эндпоинтов.
    :param expire: Время жизни кэша в секундах (по умолчанию 1 час).
    """

    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_kwargs = {k: v for k, v in kwargs.items() if k != "service"}
            cache_key = f"{func.__module__}:{func.__name__}:{cache_kwargs}"
            logger.info(f"Checking cache for key: {cache_key}")

            cached_data = await cache.get(cache_key)
            if cached_data:
                logger.info(f"Cache hit for key: {cache_key}")
                return deserialize_cached_data(cached_data)

            logger.info(f"Cache miss for key: {cache_key}")
            result = await func(*args, **kwargs)

            serialized_result = serialize_for_cache(result)
            await cache.set(cache_key, serialized_result, ttl=expire)
            logger.info(f"Data cached for key: {cache_key}")
            return result

        return wrapper

    return decorator


def serialize_for_cache(data: Any) -> Any:
    """
    Сериализует данные для хранения в кэше.
    """
    if isinstance(data, (date, datetime)):
        return data.isoformat()
    elif isinstance(data, list):
        return [serialize_for_cache(item) for item in data]
    elif isinstance(data, dict):
        return {key: serialize_for_cache(value) for key, value in data.items()}
    elif hasattr(data, "to_dict"):
        return data.to_dict()
    else:
        return data


def deserialize_cached_data(data: Any) -> Any:
    """
    Десериализует данные из кэша.
    """
    if isinstance(data, str):
        try:
            return (
                datetime.fromisoformat(data)
                if "T" in data
                else date.fromisoformat(data)
            )
        except ValueError:
            return data
    elif isinstance(data, list):
        return [deserialize_cached_data(item) for item in data]
    elif isinstance(data, dict):
        return {key: deserialize_cached_data(value) for key, value in data.items()}
    else:
        return data


def schedule_cache_reset():
    """
    Настройка сброса кэша по расписанию.
    """
    if settings.cache_reset_time:
        try:
            reset_hour, reset_minute = map(int, settings.cache_reset_time.split(":"))
            scheduler = BackgroundScheduler()
            scheduler.add_job(
                clear_cache,
                trigger=CronTrigger(hour=reset_hour, minute=reset_minute),
            )
            scheduler.start()
            print(f"Cache reset scheduled at {settings.cache_reset_time} every day.")
        except Exception as e:
            print(f"Failed to schedule cache reset: {e}")


async def clear_cache():
    """
    Очистка всего кэша в Redis.
    """
    await cache.clear()
    print(f"Cache cleared at {settings.cache_reset_time}")
