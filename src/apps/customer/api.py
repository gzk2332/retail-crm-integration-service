from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from apps.customer.dependencies import get_customer_service
from apps.customer.schemas import CustomerCreateSchema, CustomerListFilter, CustomerListResponseSchema
from apps.customer.services.customer_service import CustomerService
from core.schemas import MessageResponseSchema

router = APIRouter(prefix='/customers', tags=['customers'], default_response_class=JSONResponse)


@router.get('', status_code=status.HTTP_200_OK)
async def get_customers(
    customer_service: Annotated[CustomerService, Depends(get_customer_service)],
    filters: Annotated[CustomerListFilter, Depends()],
) -> CustomerListResponseSchema:
    return await customer_service.get_customers(filters=filters)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreateSchema,
    customer_service: Annotated[CustomerService, Depends(get_customer_service)],
) -> MessageResponseSchema:
    return await customer_service.create_customer(customer_data=customer_data)
