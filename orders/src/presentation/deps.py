from redis.asyncio import Redis
from src.infra.redis.base import redis_client


def get_redis_client() -> Redis:
    return redis_client