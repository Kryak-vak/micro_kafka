from enum import StrEnum

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


class SchemaRegistryConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_ignore_empty=True,
        extra="ignore",
        env_prefix="SCHEMA_REGISTRY_"
    )
    
    url: str


class TopicsEnum(StrEnum):
    NEW_ORDERS = "new_orders"


kafka_config = KafkaConfig()  # type: ignore
schema_registry_config = SchemaRegistryConfig().model_dump()  # type: ignore


order_producer_config = {
    'bootstrap.servers': kafka_config.bootstrap_server,
    'enable.idempotence': True,
    'acks': 1,
}



