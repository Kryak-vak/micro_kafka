from typing import Any
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.orders.dto import OrderDTO, OutboxMessageDTO
from src.infra.db.schema import Item, Order, OutboxMessage


class OrderRepository:
    schema = Order
    dto = OrderDTO

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, dto: OrderDTO):
        stmt = (
            insert(self.schema)
            .values(dto.model_dump(exclude={"items"}))
            .returning(self.schema)
        )

        result = await self.session.scalars(stmt)
        return self._to_dto(result.one())

    async def update(self, pk: int | UUID, dto: OrderDTO) -> OrderDTO:
        stmt = (
            update(self.schema)
            .where(self.schema.id == pk)  # type: ignore[attr-defined]
            .values(dto.model_dump(exclude_none=True))
            .returning(self.schema)
        )

        result = await self.session.scalars(stmt)
        return self._to_dto(result.one())

    async def get(self, **kwargs: Any) -> OrderDTO | None:
        stmt = select(self.schema).filter_by(**kwargs)

        result = await self.session.scalars(stmt)
        obj = result.one_or_none()

        return self._to_dto(obj) if obj else None
    
    def _to_dto(self, obj: Order, from_attributes: bool = True) -> OrderDTO:
        # return self.dto.model_validate(obj, from_attributes=from_attributes)
        return self.dto(
            id=obj.id,
            user_id=obj.user_id,
            status=obj.status,
            items=[]
        )


class OutboxRepository:
    schema = OutboxMessage
    dto = OutboxMessageDTO

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, dto: OutboxMessageDTO):
        stmt = (
            insert(self.schema)
            .values(dto.model_dump())
            .returning(self.schema)
        )

        result = await self.session.scalars(stmt)
        return self._to_dto(result.one())

    async def update(self, pk: int | UUID, dto: OutboxMessageDTO) -> OutboxMessageDTO:
        stmt = (
            update(self.schema)
            .where(self.schema.id == pk)  # type: ignore[attr-defined]
            .values(dto.model_dump(exclude_none=True))
            .returning(self.schema)
        )

        result = await self.session.scalars(stmt)
        return self._to_dto(result.one())

    async def get(self, **kwargs: Any) -> OutboxMessageDTO | None:
        stmt = select(self.schema).filter_by(**kwargs)

        result = await self.session.scalars(stmt)
        obj = result.one_or_none()

        return self._to_dto(obj) if obj else None

    async def filter(self, **kwargs: Any) -> list[OutboxMessageDTO]:
        stmt = select(self.schema).filter_by(**kwargs)
        
        result = await self.session.scalars(stmt)
        return [
            self._to_dto(obj)
            for obj in result.all()
        ]
    
    def _to_dto(
        self, obj: OutboxMessage, from_attributes: bool = True
    ) -> OutboxMessageDTO:
        return self.dto.model_validate(obj, from_attributes=from_attributes)

