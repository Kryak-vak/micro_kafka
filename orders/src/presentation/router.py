from fastapi import APIRouter
from src.presentation.routes.orders.router import router as orders_router

router = APIRouter()
router.include_router(orders_router, prefix="/orders", tags=["orders"])
