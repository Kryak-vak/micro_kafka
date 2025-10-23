from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from src.common_types import OrderStatus, OutboxTopic


class OrderBaseDTO(BaseModel):
    user_id: UUID
    
    items: list["OrderItemDTO"] = Field(default_factory=list)


class OrderDTO(OrderBaseDTO):
    id: UUID
    status: OrderStatus

    model_config = ConfigDict(from_attributes=True)


class OrderItemDTO(BaseModel):
    name: str
    price: int
    
    count: int

    model_config = ConfigDict(from_attributes=True)


class OutboxMessageDTO(BaseModel):
    topic: OutboxTopic
    payload: dict

    sent: bool = False
    sent_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

