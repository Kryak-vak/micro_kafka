from typing import cast

from redis.asyncio.client import Redis

from src.infra.redis.mixins import (
    BaseKeyValueRepository,
    BaseStreamRepository,
    KeySetMixin,
    RedisPrimitive,
    StreamProduceMixin,
)


class RedisOrderRepository(BaseKeyValueRepository, KeySetMixin):
    def __init__(self, redis_client: Redis) -> None:
        super().__init__(
            redis_client=redis_client,
            key_namespace="order_status:",
            default_exp=3600 * 24
        )


class RedisLogRepository(BaseStreamRepository, StreamProduceMixin):
    def __init__(
        self,
        redis_client: Redis,
        stream_suffix: str
    ) -> None:
        super().__init__(
            redis_client=redis_client,
            stream_suffix=stream_suffix,
            stream_namespace="logs",
            expire=3600 * 24 * 30
        )
    
    async def create(self, level: str, message: str) -> None:
        data = cast(dict[str, RedisPrimitive], {
            "message": message,
            "level": level
        })
        
        await self.add(data)
