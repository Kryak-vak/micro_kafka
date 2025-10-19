from redis.asyncio.client import Redis
from redis.typing import ExpiryT

RedisPrimitive = str | int | float | bytes
RedisHash = dict[str, str]


class AbstractRedisRepository:
    def __init__(
            self, redis_client: Redis,
            key_namespace: str | None = None,
            default_exp: int = 300
        ) -> None:
        self.key_namespace = key_namespace if key_namespace else ""
        self.redis_client: Redis = redis_client
        self.default_exp = default_exp
    
    def _add_namespace_to_key(self, key: str) -> str:
        return f"{self.key_namespace}{key}"
    
    async def create(
            self, key: str,
            value: RedisPrimitive = "ok",
            exp: ExpiryT | None = None,
            use_default_expiry: bool = False
        ) -> None:
        if exp is None and use_default_expiry:
            exp = self.default_exp

        key = self._add_namespace_to_key(key)
        await self.redis_client.set(name=key, value=value, ex=exp)

    async def create_hash(
            self, key: str,
            mapping: RedisHash,
            exp: ExpiryT | None = None,
            use_default_expiry: bool = False
        ) -> None:
        if exp is None and use_default_expiry:
            exp = self.default_exp
        
        key = self._add_namespace_to_key(key)
        await self.redis_client.hset(key, mapping=mapping)  # type: ignore[reportGeneralTypeIssues]
        
        if exp:
            await self.redis_client.expire(key, exp)
    
    async def get(self, key: str) -> str | None:
        key = self._add_namespace_to_key(key)
        return await self.redis_client.get(key)
    
    async def delete(self, key: str) -> None:
        key = self._add_namespace_to_key(key)
        await self.redis_client.delete(key)


class RedisOrderRepository(AbstractRedisRepository):
    def __init__(self, redis_client: Redis) -> None:
        super().__init__(
            redis_client=redis_client,
            key_namespace="order_status:",
            default_exp=3600 * 24
        )