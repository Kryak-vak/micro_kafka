from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka.serialization import (
    StringSerializer,
)
from pydantic import BaseModel

from src.config.kafka import schema_registry_config
from src.infra.kafka.schemas import order_schema_str

schema_registry_client = SchemaRegistryClient(schema_registry_config)


def str_to_dict(dto: BaseModel):
    return dto.model_dump()


def creat_json_serializer(schema_str):
    return JSONSerializer(
        schema_str, schema_registry_client, str_to_dict
    )


order_json_serializer = creat_json_serializer(order_schema_str)

string_serializer = StringSerializer('utf_8')


