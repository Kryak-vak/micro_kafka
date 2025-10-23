import logging
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from src.application.orders.dto import OrderBaseDTO, OrderDTO, OutboxMessageDTO
from src.application.orders.exceptions import OrderNotFoundException
from src.common_types import OrderStatus, OutboxTopic
from src.infra.db.repositories import OrderRepository, OutboxRepository
from src.infra.redis.repositories import RedisLogRepository, RedisOrderRepository

logger = logging.getLogger(__name__)


class OrderProduceService:
    def __init__(
            self,
            session: AsyncSession,
            order_repo: OrderRepository,
            outbox_repo: OutboxRepository,
            log_repo: RedisLogRepository,
    ) -> None:
        self.session = session
        self.order_repo = order_repo
        self.outbox_repo = outbox_repo
        self.log_repo = log_repo

    async def handle_order(self, order_in: OrderBaseDTO) -> UUID:
        order_id = uuid4()

        order_dto = OrderDTO(
            id=order_id,
            status=OrderStatus.PENDING,
            **order_in.model_dump()
        )
        outbox_dto = OutboxMessageDTO(
            topic=OutboxTopic.ORDERS,
            payload=order_dto.model_dump(mode="json")
        )

        await self.create_order(order_dto, outbox_dto)

        return order_id
    
    async def create_order(
        self, order_dto: OrderDTO, outbox_dto: OutboxMessageDTO
    ) -> None:
        # TODO handle/log exceptions
        async with self.session.begin():
            await self.order_repo.create(order_dto)
            await self.outbox_repo.create(outbox_dto)

class OrderStatusService:
    def __init__(
        self,
        order_repo: OrderRepository,
        redis_repo: RedisOrderRepository,
    ) -> None:
        self.order_repo = order_repo
        self.redis_repo = redis_repo
    
    async def get_order_status(self, order_id: UUID) -> OrderStatus:
        order_dto = await self.order_repo.get(id=order_id)

        if not order_dto:
            raise OrderNotFoundException(order_id=order_id)
        
        return order_dto.status

