from uuid import UUID

from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka.serialization import (
    StringSerializer,
)
from pydantic import BaseModel

from src.config.kafka import schema_registry_config
from src.infra.kafka.schemas import order_schema_str

schema_registry_client = SchemaRegistryClient(schema_registry_config)


def str_to_dict(dto: BaseModel, ctx):
    return dto.model_dump()


def serialize_base_model(obj: BaseModel, _):
    def convert(value):
        if isinstance(value, UUID):
            return str(value)
        elif isinstance(value, BaseModel):
            return serialize_base_model(value, None)
        elif isinstance(value, list):
            return [convert(v) for v in value]
        elif isinstance(value, dict):
            return {k: convert(v) for k, v in value.items()}
        return value

    return {k: convert(v) for k, v in obj.model_dump().items()}


def creat_json_serializer(schema_str):
    return JSONSerializer(
        schema_str, # type: ignore
        schema_registry_client,
        serialize_base_model
    )


order_json_serializer = creat_json_serializer(order_schema_str)

string_serializer = StringSerializer('utf_8')


