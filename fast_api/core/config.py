from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    db_user: str = "spimex_user"
    db_password: str = "spimex_password"
    db_name: str = "spimex_db"
    db_host: str = "localhost"
    db_port: int = 5432

    redis_host: str = "localhost"
    redis_port: int = 6379

    cache_reset_time: Optional[str] = "14:11"

    class Config:
        env_file = ".env"


settings = Settings()