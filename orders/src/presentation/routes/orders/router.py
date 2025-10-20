from fastapi import APIRouter, Depends, status

from src.application.orders.dto import OrderBaseDTO
from src.application.orders.services import OrderProduceService
from src.presentation.routes.orders.deps import get_order_produce_service
from src.presentation.routes.orders.schemas import (
    OrderAcceptedResponse,
    OrderIn,
    OrderStatus,
)

router = APIRouter()


@router.post(
        "/",
        response_model=OrderAcceptedResponse,
        status_code=status.HTTP_202_ACCEPTED
    )
async def new_order(
    order_in: OrderIn,
    order_service: OrderProduceService = Depends(get_order_produce_service)
):
    order_base_dto = OrderBaseDTO(
        **order_in.model_dump()
    )
    order_id = await order_service.handle_order(order_base_dto)

    return OrderAcceptedResponse(
        message="Order has been accepted for processing.",
        order_id=order_id,
        status=OrderStatus.ACCEPTED,
    )
