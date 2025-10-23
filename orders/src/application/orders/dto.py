from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class OrderBaseDTO(BaseModel):
    user_id: UUID
    
    items: list["OrderItemDTO"]


class OrderDTO(OrderBaseDTO):
    id: UUID


class OrderItemDTO(BaseModel):
    name: str
    price: int
    
    count: int


class OutboxMessageDTO(BaseModel):
    id: UUID

    topic: str
    payload: dict

    sent: bool = False
    sent_at: datetime | None = None

