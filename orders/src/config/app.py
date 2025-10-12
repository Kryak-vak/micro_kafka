from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = ENV_DIR / ".env"


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_ignore_empty=True,
        extra="ignore",
    )

    project_name: str
    api_v1_str: str = "/api/v1"


app_config = AppConfig()  # type: ignore
