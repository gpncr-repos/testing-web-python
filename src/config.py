from pathlib import Path

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).parent / ".env"


class Settings(BaseSettings):
    db_url: AnyUrl

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


settings = Settings()
