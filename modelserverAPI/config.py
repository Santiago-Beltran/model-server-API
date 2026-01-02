from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENV_STATE: Optional[str] = None
    API_KEY_NAME: Optional[str] = None
    API_KEY: Optional[str] = None
    REQUEST_LIMIT_PER_MINUTE: Optional[str] = None
    REQUEST_LIMIT_PER_SECOND: Optional[str] = None


class DevConfig(Settings):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class TestConfig(Settings):
    model_config = SettingsConfigDict(env_prefix="TEST_")

    REQUEST_LIMIT_PER_SECOND: Optional[str] = "5/second"
    REQUEST_LIMIT_PER_MINUTE: Optional[str] = "10/minute"


class ProdConfig(Settings):
    model_config = SettingsConfigDict(env_prefix="PROD_")


@lru_cache
def get_config(env_state: str):
    configs = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}
    return configs[env_state]()


config = get_config(Settings().ENV_STATE)
