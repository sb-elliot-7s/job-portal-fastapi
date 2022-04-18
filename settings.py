from functools import lru_cache
from pydantic import BaseSettings, HttpUrl, PostgresDsn


class Settings(BaseSettings):
    database_url: PostgresDsn
    secret_key: str

    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    domain: HttpUrl

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Settings:
    return Settings()
