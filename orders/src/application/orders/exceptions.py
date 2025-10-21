from uuid import UUID


class OrderDomainException(Exception):
    """Base exception all exceptions related to Orders."""
    pass


class OrderNotFoundException(OrderDomainException):
    """Raised when the order ID does not exist in the repository."""
    def __init__(self, order_id: UUID):
        self.order_id = order_id
        super().__init__(f"Order with id {order_id} not found")

    def __str__(self) -> str:
        return f"Order with id {self.order_id} not found"
