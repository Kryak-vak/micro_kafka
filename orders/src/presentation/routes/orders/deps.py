from fastapi import Depends
from redis.asyncio import Redis

from src.application.orders.services import OrderProduceService, OrderStatusService
from src.infra.db.repositories import OrderRepository
from src.infra.redis.repositories import RedisLogRepository, RedisOrderRepository
from src.presentation.deps import SessionDep, get_redis_client


def get_order_repo(
    session: SessionDep
) -> OrderRepository:
    return OrderRepository(session=session)


def get_redis_repo(
    redis_client: Redis = Depends(get_redis_client)
) -> RedisOrderRepository:
    return RedisOrderRepository(
        redis_client=redis_client
    )


def get_log_repo(
    redis_client: Redis = Depends(get_redis_client)
):
    return RedisLogRepository(
        redis_client=redis_client,
        stream_suffix="order_produce"
    )


def get_order_produce_service(
    session: SessionDep,
    order_repo: OrderRepository = Depends(get_order_repo),
    log_repo: RedisLogRepository = Depends(get_log_repo),
) -> OrderProduceService:
    return OrderProduceService(
        session=session,
        order_repo=order_repo,
        log_repo=log_repo
    )


def get_order_status_service(
    order_repo: OrderRepository = Depends(get_order_repo),
    redis_repo: RedisOrderRepository = Depends(get_order_repo),
) -> OrderStatusService:
    return OrderStatusService(
        order_repo=order_repo,
        redis_repo=redis_repo,
    )
