from pydantic_settings import BaseSettings, SettingsConfigDict
from src.config.app import ENV_FILE


class KafkaConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_ignore_empty=True,
        extra="ignore",
        env_prefix="KAFKA_"
    )
    
    bootstrap_server: str


kafka_config = KafkaConfig()  # type: ignore
