import logging
from uuid import UUID, uuid4

from confluent_kafka import Message
from confluent_kafka.error import KafkaError
from confluent_kafka.serialization import (
    MessageField,
    SerializationContext,
)
from fastapi.concurrency import run_in_threadpool
from src.application.orders.dto import OrderBaseDTO, OrderDTO
from src.common_types import OrderStatus
from src.config.kafka import TopicsEnum
from src.infra.kafka.producers import order_producer
from src.infra.kafka.registry import order_json_serializer, string_serializer
from src.infra.redis.repositories import RedisOrderRepository

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, redis_repo: RedisOrderRepository):
        self.redis_repo = redis_repo

    async def handle_order(self, order_in: OrderBaseDTO) -> UUID:
        order_id = uuid4()

        order_dto = OrderDTO(
            id=order_id,
            **order_in.model_dump()
        )

        await run_in_threadpool(self.send_order_to_topic, order_dto)
        await self.redis_repo.create(str(order_dto.id), OrderStatus.PENDING)

        return order_id

    def order_to_dict(self, order_dto: OrderDTO) -> dict:
        return order_dto.model_dump()

    @staticmethod
    def delivery_report(err: KafkaError, msg: Message) -> None:
        if err is not None:
            logger.exception(f"Delivery failed for Order {msg.key()}: {err}")
            return
        
        logger.info(
            f"Order {msg.key()} successfully produced to "
            f"{msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
        )

    async def send_order_to_topic(self, order_dto: OrderDTO) -> None:
        topic = TopicsEnum.NEW_ORDERS
        key = string_serializer(
            str(order_dto.id),
            SerializationContext(topic, MessageField.KEY)
        )
        value = order_json_serializer(
            order_dto,
            SerializationContext(topic, MessageField.VALUE)
        )

        try:
            order_producer.produce(
                topic=TopicsEnum.NEW_ORDERS,
                key=key,
                value=value,
                on_delivery=self.delivery_report
            )
        except BufferError as e:
            logger.exception(f"Producer queue is full: {e}")
        
        order_producer.poll(0)


