from enum import StrEnum


class OrderStatus(StrEnum):
    ACCEPTED = "accepted"
    FAILED = "failed"
    PENDING = "pending"
    SHIPPED = "shipped"
    COMPLETED = "completed"


class OutboxTopic(StrEnum):
    ORDERS = "orders"

