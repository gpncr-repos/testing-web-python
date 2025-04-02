from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).parent / ".env"


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "calculator"
    db_user: str
    db_pass: str

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


settings = Settings()
