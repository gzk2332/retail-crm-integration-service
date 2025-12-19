from functools import lru_cache
from pathlib import Path
from typing import Literal, TypedDict

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent
BASE_DIR = PROJECT_ROOT.parent


class BaseConfig(TypedDict):
    env_file: Path
    env_file_encoding: str
    extra: Literal['ignore']


BASE_CONFIG: BaseConfig = {
    'env_file': BASE_DIR / '.env',
    'env_file_encoding': 'utf-8',
    'extra': 'ignore',
}


class RetailCRMSettings(BaseSettings):
    API_URL: str
    API_PREFIX: str = 'api'
    API_VERSION: str = 'v5'
    API_KEY: str

    model_config = SettingsConfigDict(**BASE_CONFIG, env_prefix='retail_crm_')


class AppSettings(BaseSettings):
    # App
    APP_NAME: str = 'RetailCRM Integration Service'
    TIMEZONE: str = 'UTC'

    # Env
    ENV: str = 'dev'

    # API
    API_PREFIX: str = '/api'
    AUTO_RELOAD: bool = False
    HOST: str = '0.0.0.0'
    PORT: int = 8000

    # Apps
    APPLICATIONS_MODULE: str = 'apps'
    APPLICATIONS: tuple[str, ...] = (
        'health',
        'customer',
        'order',
    )

    RetailCRM: RetailCRMSettings = RetailCRMSettings()

    model_config = SettingsConfigDict(**BASE_CONFIG, use_enum_values=True)

    def get_apps_list(self) -> tuple[str, ...]:
        return tuple(f'{self.APPLICATIONS_MODULE}.{app}' for app in self.APPLICATIONS)


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
