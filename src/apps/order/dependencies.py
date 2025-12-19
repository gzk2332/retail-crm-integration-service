from apps.order.services.order_service import OrderService


def get_order_service() -> OrderService:
    return OrderService()
