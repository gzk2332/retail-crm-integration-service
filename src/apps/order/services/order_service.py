from apps.order.schemas import (
    OrderCreateResponseSchema,
    OrderCreateShema,
    OrderListFilter,
    OrderListResponseSchema,
    PaymentCreateSchema,
)
from core.schemas import MessageResponseSchema
from integrations.retail_crm.client import RetailCRMApiClient
from integrations.retail_crm.endpoints import RetailCRMEndpoint


class OrderService:
    def __init__(self) -> None:
        self.retail_client = RetailCRMApiClient()

    async def get_orders(self, customer_id: int, filters: OrderListFilter) -> OrderListResponseSchema:
        query_params_dict = filters.model_dump(exclude_none=True, by_alias=True, mode='json')
        query_params_dict['customerId'] = customer_id

        response_data = await self.retail_client.make_request(
            data=None, filters=query_params_dict, endpoint=RetailCRMEndpoint.GET_ORDERS
        )
        return OrderListResponseSchema.model_validate(response_data)

    async def create_order(self, customer_id: int, order_data: OrderCreateShema) -> OrderCreateResponseSchema:
        order_payload = order_data.model_dump(exclude_none=True, by_alias=True, mode='json')
        order_payload['customer'] = {'id': customer_id}

        response_data = await self.retail_client.make_request(
            data={'order': order_payload}, filters=None, endpoint=RetailCRMEndpoint.CREATE_ORDER
        )
        return OrderCreateResponseSchema.model_validate(response_data)

    async def create_payment_for_order(self, order_id: int, payment_data: PaymentCreateSchema) -> MessageResponseSchema:
        payment_payload = payment_data.model_dump(exclude_none=True, by_alias=True, mode='json')
        payment_payload['order'] = {'id': order_id}

        response_data = await self.retail_client.make_request(
            data={'payment': payment_payload}, filters=None, endpoint=RetailCRMEndpoint.CREATE_PAYMENT_FOR_ORDER
        )
        return MessageResponseSchema(id=response_data['id'], message='Payment created successfully.')
