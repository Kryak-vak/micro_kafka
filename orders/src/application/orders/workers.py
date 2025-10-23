import asyncio
import logging
from uuid import UUID, uuid4

from confluent_kafka import Message
from confluent_kafka.error import KafkaError, KafkaException
from confluent_kafka.serialization import (
    MessageField,
    SerializationContext,
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.orders.dto import OrderBaseDTO, OrderDTO, OutboxMessageDTO
from src.application.orders.exceptions import OrderNotFoundException
from src.common_types import OrderStatus, OutboxTopic
from src.config.kafka import TopicsEnum
from src.infra.db.repositories import OrderRepository, OutboxRepository
from src.infra.kafka.producers import order_producer
from src.infra.kafka.registry import order_json_serializer, string_serializer
from src.infra.redis.repositories import RedisLogRepository, RedisOrderRepository
from src.utils.event_loop import get_main_loop
from src.utils.kafka import is_retriable_kafka_error
from tenacity import (
    retry,
    retry_if_exception,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


class OrderProduceWorker:
    
    def delivery_report(self, err: KafkaError, msg: Message) -> None:
        key = UUID(msg.key().decode("utf-8"))
        partition = msg.partition().decode("utf-8") if msg.partition() else None
        offset = msg.offset()

        if err is not None:
            self._create_status_task(key, OrderStatus.FAILED)

            self._log(
                "error",
                f"Delivery failed for Order {key}: {err}",
                to_task=True
            )
            return
        
        self._create_status_task(key, OrderStatus.ACCEPTED)

        self._log(
            "info",
            (f"Order {key} successfully produced to "
             f"{msg.topic()} [{partition}] at offset {offset}"),
            to_task=True
        )

    def send_order_to_topic(self, order_dto: OrderDTO) -> None:
        topic = TopicsEnum.NEW_ORDERS

        # TODO Serialization error handling
        key = string_serializer(
            str(order_dto.id),
            SerializationContext(topic, MessageField.KEY)
        )
        value = order_json_serializer(
            order_dto,
            SerializationContext(topic, MessageField.VALUE)
        )

        try:
            self._produce_with_retry(topic, key, value) # type: ignore
        except (KafkaException, BufferError) as e:
            self._log(
                "exception",
                f"Kafka produce failed after retries: {e}",
                to_task=True
            )
    
    @retry(
        retry=(
            retry_if_exception(is_retriable_kafka_error) |
            retry_if_exception_type(BufferError)
        ),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=0.5, min=1, max=10),
        reraise=True,
    )
    def _produce_with_retry(self, topic: str, key: bytes, value: bytes) -> None:
        try:
            order_producer.produce(
                topic=topic,
                key=key,
                value=value,
                on_delivery=self.delivery_report
            )
        except BufferError:
            order_producer.poll(1)
            raise
        else:
            order_producer.poll(0)
    
    async def _update_order_status(self, order_id: UUID, status: OrderStatus) -> None:
        await self.order_repo.create(str(order_id), status)
    
    def _create_status_task(self, order_id: UUID, status: OrderStatus) -> None:
        asyncio.run_coroutine_threadsafe(
            self._update_order_status(order_id, status),
            get_main_loop()
        )
    
    def _log(self, level: str, log_message: str, to_task: bool = False) -> None:
        # TODO Upgrade logger logic to a special Logger class to avoid this atrocity
        logger_funcs = {
            "info": logger.info,
            "error": logger.error,
            "exception": logger.exception
        }

        logger_func = logger_funcs.get(level)
        assert logger_func is not None

        logger_func(log_message)

        if to_task:
            self._create_log_task(level, log_message)

    def _create_log_task(self, level: str, log_message: str) -> None:
        asyncio.run_coroutine_threadsafe(
            self.log_repo.create(level, log_message),
            get_main_loop()
        )


