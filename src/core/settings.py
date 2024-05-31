from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_user: str
    db_pass: str
    db_host: str
    db_port: int
    db_name: str

    jws_alg: str = "RS256"
    access_token_exp_mins: int = 30
    secret_key_path: str
    public_key_path: str

    model_config = SettingsConfigDict(env_file=Path(__file__).parent / '../../.env')


__settings = Settings()


@lru_cache()  # just to make dep injections easier
def get_settings() -> Settings:
    return __settings


@lru_cache()
def get_rsa_private() -> str:
    with open(get_settings().secret_key_path, encoding='utf-8') as f:
        return f.read()

@lru_cache()
def get_rsa_public() -> str:
    with open(get_settings().public_key_path, encoding='utf-8') as f:
        return f.read()


TORTOISE_ORM: dict = {
    "connections": {
        "default": f"asyncpg://{__settings.db_user}:{__settings.db_pass}@{__settings.db_host}:{__settings.db_port}/{__settings.db_name}"},
    "apps": {
        "main": {
            "models": ["aerich.models", "core.db.models"],
            "default_connection": "default",
        },
    },
}
