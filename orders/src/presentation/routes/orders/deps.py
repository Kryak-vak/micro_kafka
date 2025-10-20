from fastapi import Depends
from redis.asyncio import Redis

from src.application.orders.services import OrderProduceService
from src.infra.redis.repositories import RedisLogRepository, RedisOrderRepository
from src.presentation.deps import get_redis_client


def get_order_repo(redis_client: Redis = Depends(get_redis_client)):
    return RedisOrderRepository(redis_client=redis_client)


def get_log_repo(redis_client: Redis = Depends(get_redis_client)):
    return RedisLogRepository(
        redis_client=redis_client,
        stream_suffix="order_produce"
    )


def get_order_produce_service(
        redis_repo: RedisOrderRepository = Depends(get_order_repo),
        log_repo: RedisLogRepository = Depends(get_log_repo),
    ) -> OrderProduceService:
    return OrderProduceService(
        order_repo=redis_repo,
        log_repo=log_repo
    )
