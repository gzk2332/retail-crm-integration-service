from decimal import Decimal

from pydantic import AliasPath, BaseModel, Field

from apps.order.enums import PaymentTypeEnums
from core.schemas import BaseFilter, PaginationSchema


class OrderListFilter(BaseFilter):
    pass


class OrderItemShema(BaseModel):
    product_name: str = Field(serialization_alias='productName')
    quantity: float = Field(default=1.0, gt=0)
    initial_price: Decimal = Field(serialization_alias='initialPrice', gt=0)


class OrderCreateShema(BaseModel):
    number: str
    items: list[OrderItemShema]


class OrderCreateResponseSchema(BaseModel):
    order_id: int = Field(alias='id')
    order_number: str = Field(validation_alias=AliasPath('order', 'number'))
    total_summ: Decimal = Field(validation_alias=AliasPath('order', 'totalSumm'))
    created_at: str = Field(validation_alias=AliasPath('order', 'createdAt'))


class OrderItemReadSchema(BaseModel):
    id: int
    name: str = Field(validation_alias=AliasPath('offer', 'displayName'))
    quantity: float
    initial_price: Decimal = Field(validation_alias='initialPrice')


class OrderPaymentSchema(BaseModel):
    id: int
    type: str
    amount: Decimal
    comment: str | None = None
    status: str | None = None


class OrderReadSchema(BaseModel):
    id: int
    number: str
    status: str
    total_summ: Decimal = Field(validation_alias='totalSumm')
    created_at: str = Field(validation_alias='createdAt')
    items: list[OrderItemReadSchema] = []
    payments: dict[str, OrderPaymentSchema] = {}


class OrderListResponseSchema(BaseModel):
    orders: list[OrderReadSchema]
    pagination: PaginationSchema


class PaymentCreateSchema(BaseModel):
    amount: Decimal = Field(gt=0)
    comment: str | None = None
    payment_type: PaymentTypeEnums | str = Field(default=PaymentTypeEnums.CASH, alias='type')


class PaymentResponseSchema(BaseModel):
    payment_id: int = Field(alias='id')
