from redis.asyncio.client import Redis
from src.config.redis import redis_config

redis_client = Redis(
    host=redis_config.host,
    port=redis_config.port,
    decode_responses=True
)
