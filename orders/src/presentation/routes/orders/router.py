from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.application.orders.dto import OrderBaseDTO
from src.application.orders.exceptions import OrderNotFoundException
from src.application.orders.services import OrderProduceService, OrderStatusService
from src.presentation.routes.orders.deps import (
    get_order_produce_service,
    get_order_status_service,
)
from src.presentation.routes.orders.schemas import (
    OrderAcceptedResponse,
    OrderIn,
    OrderInfo,
    OrderStatus,
)

router = APIRouter()


@router.post(
        "/",
        response_model=OrderAcceptedResponse,
        status_code=status.HTTP_202_ACCEPTED
    )
async def create_order(
    order_in: OrderIn,
    order_produce_service: OrderProduceService = Depends(get_order_produce_service)
) -> OrderAcceptedResponse:
    order_base_dto = OrderBaseDTO(
        **order_in.model_dump()
    )
    order_id = await order_produce_service.handle_order(order_base_dto)

    return OrderAcceptedResponse(
        message="Order has been accepted for processing.",
        order=OrderInfo(
            id=order_id,
            status=OrderStatus.PENDING,
        ),
    )


@router.get(
        "/{order_id}",
        response_model=OrderInfo,
        status_code=status.HTTP_200_OK,
        responses={
            404: {
                "description": "Order with the given ID was not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "Order with id 123 not found"
                        }
                    }
                },
            },
        },
    )
async def get_order(
    order_id: Annotated[UUID, Path(title="ID of the order to get")],
    order_status_service: OrderStatusService = Depends(get_order_status_service)
) -> OrderInfo:
    try:
        order_status = await order_status_service.get_order_status(order_id)
    except OrderNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    return OrderInfo(
        id=order_id,
        status=order_status
    )