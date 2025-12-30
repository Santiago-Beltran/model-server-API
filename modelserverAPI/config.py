from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    ENV_STATE: Optional[str] = None


class DevConfig(Settings):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class TestConfig(Settings):
    model_config = SettingsConfigDict(env_prefix="TEST_")


class ProdConfig(Settings):
    model_config = SettingsConfigDict(env_prefix="PROD_")


@lru_cache
def get_config(env_state: str):
    configs = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}
    return Settings()


config = get_config(Settings().ENV_STATE)
