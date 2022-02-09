from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    DEBUG: bool = True
    BASE_DIR: Path = BASE_DIR
    DATABASE_URI: str = 'sqlite://database.sqlite'

    CENSYS_ID: str
    CENSYS_SECRET: str
    

    class Config:
        env_prefix = ''
        env_file = BASE_DIR.joinpath('.env')


@lru_cache
def _build_settings():
    return Settings()


settings = _build_settings()
