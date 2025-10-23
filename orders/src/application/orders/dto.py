from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from src.common_types import OrderStatus, OutboxTopic


class OrderBaseDTO(BaseModel):
    user_id: UUID
    
    items: list["OrderItemDTO"]


class OrderDTO(OrderBaseDTO):
    id: UUID
    status: OrderStatus


class OrderItemDTO(BaseModel):
    name: str
    price: int
    
    count: int


class OutboxMessageDTO(BaseModel):
    id: UUID | None = None

    topic: OutboxTopic
    payload: dict

    sent: bool = False
    sent_at: datetime | None = None

