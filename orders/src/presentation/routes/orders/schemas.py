from uuid import UUID

from pydantic import BaseModel

from src.common_types import OrderStatus


class OrderIn(BaseModel):
    user_id: UUID

    items: list["OrderItemIn"]


class OrderItemIn(BaseModel):
    name: str
    price: int
    
    count: int


class OrderInfo(BaseModel):
    id: UUID
    status: OrderStatus


class OrderAcceptedResponse(BaseModel):
    message: str
    order: OrderInfo

