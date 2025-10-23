from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Enum, ForeignKey, MetaData, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.common_types import OrderStatus


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)

    user_id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)

    items: Mapped[list["Item"]] = relationship(
        back_populates="wallet", cascade="all, delete-orphan"
    )

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, native_enum=False),
        default=OrderStatus.PENDING
    )

    def __repr__(self):
        return f"<Order(id={self.id}, status={self.status})>"


class Item(Base):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id"))
    order: Mapped["Order"] = relationship(back_populates="items")

    name: Mapped[str]
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2), default=Decimal("0.00"), nullable=False
    )
    count: Mapped[int]

    def __repr__(self):
        return f"<Item(id={self.id}, name{self.name})>"