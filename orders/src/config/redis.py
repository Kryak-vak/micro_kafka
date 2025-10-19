from pydantic_settings import BaseSettings, SettingsConfigDict
from src.config.app import ENV_FILE


class RedisConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_file=ENV_FILE,
        extra="ignore"
    )

    host: str
    port: int = 6379


redis_config = RedisConfig()  # type: ignore
