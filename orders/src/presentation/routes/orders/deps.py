from fastapi import Depends
from redis.asyncio import Redis

from src.application.orders.services import OrderService
from src.infra.redis.repositories import RedisOrderRepository
from src.presentation.deps import get_redis_client


def get_redis_order_repo(redis_client: Redis = Depends(get_redis_client)):
    return RedisOrderRepository(redis_client=redis_client)


def get_order_service(
        redis_repo: RedisOrderRepository = Depends(get_redis_order_repo),
    ) -> OrderService:
    return OrderService(
        redis_repo=redis_repo,
    )
