from confluent_kafka import Producer
from src.infrastructure.kafka.config import config

producer = Producer(config)

