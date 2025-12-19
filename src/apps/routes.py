from fastapi import APIRouter

from apps.customer.api import router as customer_router
from apps.health.api import router as health_router
from apps.order.api import order_customer_router as order_customer_router
from apps.order.api import order_router

routers: tuple[APIRouter, ...] = (
    health_router,
    customer_router,
    order_customer_router,
    order_router,
)
