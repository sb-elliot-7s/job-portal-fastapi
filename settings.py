from functools import lru_cache
from pydantic import BaseSettings, HttpUrl, PostgresDsn
from pathlib import Path

IMAGE_DIR = f'{Path(__file__).resolve().parent.joinpath("images")}'


class Settings(BaseSettings):
    database_url: PostgresDsn
    secret_key: str

    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    domain: HttpUrl

    key_for_pyotp: str
    two_factor_auth_interval: int

    sender: str
    sender_password: str
    google_host_smtp: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Settings:
    return Settings()
