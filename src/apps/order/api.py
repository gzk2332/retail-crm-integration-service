from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from apps.order.dependencies import get_order_service
from apps.order.schemas import (
    OrderCreateResponseSchema,
    OrderCreateShema,
    OrderListFilter,
    OrderListResponseSchema,
    PaymentCreateSchema,
)
from apps.order.services.order_service import OrderService
from core.schemas import MessageResponseSchema

order_customer_router = APIRouter(prefix='/customers', tags=['orders'], default_response_class=JSONResponse)
order_router = APIRouter(prefix='/orders', tags=['orders'], default_response_class=JSONResponse)


@order_customer_router.get('/{customer_id}/orders', status_code=status.HTTP_200_OK)
async def get_orders(
    customer_id: int,
    order_service: Annotated[OrderService, Depends(get_order_service)],
    filters: Annotated[OrderListFilter, Depends()],
) -> OrderListResponseSchema:
    return await order_service.get_orders(customer_id=customer_id, filters=filters)


@order_customer_router.post('/{customer_id}/orders', status_code=status.HTTP_201_CREATED)
async def create_order(
    customer_id: int,
    order_data: OrderCreateShema,
    order_service: Annotated[OrderService, Depends(get_order_service)],
) -> OrderCreateResponseSchema:
    return await order_service.create_order(customer_id=customer_id, order_data=order_data)


@order_router.post('/{order_id}/payments', status_code=status.HTTP_201_CREATED)
async def create_payment_for_order(
    order_id: int,
    payment_data: PaymentCreateSchema,
    order_service: Annotated[OrderService, Depends(get_order_service)],
) -> MessageResponseSchema:
    return await order_service.create_payment_for_order(order_id=order_id, payment_data=payment_data)
