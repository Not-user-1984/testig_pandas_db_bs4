from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    db_user: str = "spimex_user"
    db_password: str = "spimex_password"
    db_name: str = "spimex_db"
    db_host: str = "db"
    db_port: int = 5432

    redis_host: str = "redis"
    redis_port: int = 6379

    cache_reset_time: Optional[str] = "14:11"

    class Config:
        env_file = ".env"
        env_prefix = "POSTGRES_"
        fields = {
            "db_user": {"env": "POSTGRES_USER"},
            "db_password": {"env": "POSTGRES_PASSWORD"},
            "db_name": {"env": "POSTGRES_DB"},
            "db_host": {"env": "POSTGRES_HOST"},
            "db_port": {"env": "POSTGRES_PORT"},
            "redis_host": {"env": "REDIS_HOST"},
            "redis_port": {"env": "REDIS_PORT"},
            "cache_reset_time": {"env": "CACHE_RESET_TIME"},
        }
    @property
    def get_url(self) -> str:
        """
        Возвращает URL для подключения к базе данных.
        """
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()