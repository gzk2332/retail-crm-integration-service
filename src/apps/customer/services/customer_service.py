from apps.customer.schemas import CustomerCreateSchema, CustomerListFilter, CustomerListResponseSchema
from core.schemas import MessageResponseSchema
from integrations.retail_crm.client import RetailCRMApiClient
from integrations.retail_crm.endpoints import RetailCRMEndpoint


class CustomerService:
    def __init__(self) -> None:
        self.retail_client = RetailCRMApiClient()

    async def get_customers(self, filters: CustomerListFilter) -> CustomerListResponseSchema:
        query_params_dict = filters.model_dump(exclude_none=True, by_alias=True, exclude={'created_at'}, mode='json')

        response_data = await self.retail_client.make_request(
            data=None, filters=query_params_dict, endpoint=RetailCRMEndpoint.GET_CUSTOMERS
        )
        return CustomerListResponseSchema.model_validate(response_data)

    async def create_customer(self, customer_data: CustomerCreateSchema) -> MessageResponseSchema:
        customer_payload = {'customer': customer_data.model_dump(exclude_none=True, by_alias=True, mode='json')}

        response_data = await self.retail_client.make_request(
            data=customer_payload, filters=None, endpoint=RetailCRMEndpoint.CREATE_CUSTOMER
        )
        return MessageResponseSchema(id=response_data['id'], message='Customer created successfully.')
