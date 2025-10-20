from datetime import datetime, timezone
from typing import Protocol, cast

from redis.asyncio.client import Redis
from redis.typing import EncodableT, ExpiryT, FieldT

RedisPrimitive = str | int | float | bytes
RedisHashT = dict[str, str]


class BaseKeyValueRepository:
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


class _KeyValueDerived(Protocol):
    redis_client: Redis
    default_exp: int

    def _add_namespace_to_key(self, key: str) -> str: ...


class KeySetMixin:
    async def set(
            self: _KeyValueDerived,
            key: str,
            value: RedisPrimitive = "ok",
            exp: ExpiryT | None = None,
            use_default_expiry: bool = False
    ) -> None:
        if exp is None and use_default_expiry:
            exp = self.default_exp

        key = self._add_namespace_to_key(key)
        await self.redis_client.set(name=key, value=value, ex=exp)
    
    create = set


class KeyGetDeleteMixin:
    async def get(self: _KeyValueDerived, key: str) -> str | None:
        key = self._add_namespace_to_key(key)
        return await self.redis_client.get(key)
    
    async def delete(self: _KeyValueDerived, key: str) -> None:
        key = self._add_namespace_to_key(key)
        await self.redis_client.delete(key)


class HashSetMixin:
    async def create_hash(
            self: _KeyValueDerived,
            key: str,
            mapping: RedisHashT,
            exp: ExpiryT | None = None,
            use_default_expiry: bool = False
    ) -> None:
        if exp is None and use_default_expiry:
            exp = self.default_exp
        
        key = self._add_namespace_to_key(key)
        await self.redis_client.hset(key, mapping=mapping)  # type: ignore[reportGeneralTypeIssues]
        
        if exp:
            await self.redis_client.expire(key, exp)




class BaseStreamRepository:
    def __init__(
        self, redis_client: Redis,
        stream_suffix: str,
        stream_namespace: str | None = None,
        expire: int | None = None
    ) -> None:
        self.redis_client: Redis = redis_client
        
        if stream_namespace:
            self.stream_name = f"{stream_namespace}:{stream_suffix}"
        else:
            self.stream_name = stream_suffix
        
        self.expire = expire


class _StreamDerived(Protocol):
    redis_client: Redis
    stream_name: str


class StreamProduceMixin:
    async def add(
        self: _StreamDerived,
        data: dict[str, RedisPrimitive],
    ) -> None:
        data_timestamped = cast(dict[FieldT, EncodableT], {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **data,
        })

        await self.redis_client.xadd(
            self.stream_name,
            data_timestamped,
        )


class StreamConsumeMixin:
    async def read(
        self: _StreamDerived,
        count: int = 10,
        block_ms: int | None = None,
        start_id: str = "0",
    ) -> list[dict[str, RedisPrimitive]]:
        entries = await self.redis_client.xread(
            streams={self.stream_name: start_id},
            count=count,
            block=block_ms,
        )

        result: list[dict[str, RedisPrimitive]] = []
        if not entries:
            return result

        for _, messages in entries:
            for msg_id, fields in messages:
                result.append({
                    "id": msg_id,
                    "fields": fields,
                })

        return result

