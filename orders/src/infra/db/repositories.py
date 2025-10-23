from typing import Any
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.orders.dto import OrderDTO
from src.infra.db.schema import Order


class OrderRepository:
    schema = Order
    dto = OrderDTO

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, order_dto: OrderDTO):
        stmt = (
            insert(self.schema)
            .values(order_dto.model_dump())
            .returning(self.schema)
        )

        result = await self.session.scalars(stmt)
        return self._to_dto(result.one())

    async def update(self, pk: int | UUID, order_dto: OrderDTO) -> OrderDTO:
        stmt = (
            update(self.schema)
            .where(self.schema.id == pk)  # type: ignore[attr-defined]
            .values(order_dto.model_dump(exclude_none=True))
            .returning(self.schema)
        )

        result = await self.session.scalars(stmt)
        return self._to_dto(result.one())

    async def get(self, **kwargs: Any) -> OrderDTO | None:
        stmt = select(self.schema).filter_by(**kwargs)

        result = await self.session.scalars(stmt)
        schema_instance = result.one_or_none()

        return self._to_dto(schema_instance) if schema_instance else None
    
    def _to_dto(self, order: Order, from_attributes: bool = True) -> OrderDTO:
        return self.dto.model_validate(order, from_attributes=from_attributes)

