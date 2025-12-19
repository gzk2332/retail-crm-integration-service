from datetime import date, datetime

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, model_validator

from apps.customer.enums import CountryIsoEnums, CustomerGenderEnums
from core.schemas import BaseFilter, PaginationSchema


class CustomerListFilter(BaseFilter):
    name: str | None = None
    email: str | None = None

    date_from: date | None = Field(default=None, serialization_alias='dateFrom')
    date_to: date | None = Field(default=None, serialization_alias='dateTo')
    created_at: date | None = None

    @model_validator(mode='after')
    def validate_dates(self) -> 'CustomerListFilter':
        if self.created_at:
            if self.date_from or self.date_to:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Use either 'created_at' or 'date_from'/'date_to', not both",
                )
            self.date_from = self.date_to = self.created_at

        if self.date_from and self.date_to and self.date_to < self.date_from:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='date_to must be >= date_from')
        return self


class CustomerPhoneSchema(BaseModel):
    number: str = Field(pattern=r'^\+\d{8,15}$')


class CustomerAddressSchema(BaseModel):
    index: str | None = None
    country_iso: CountryIsoEnums | None = Field(default=None, serialization_alias='countryIso')
    region: str | None = None
    city: str | None = None
    street: str | None = None
    building: str | None = None
    flat: str | None = None


class CustomerCreateSchema(BaseModel):
    first_name: str = Field(serialization_alias='firstName', max_length=200)
    last_name: str = Field(serialization_alias='lastName', max_length=200)
    email: str = Field(pattern=r'^[^\s@]+@[^\s@]+\.[^\s@]+$', max_length=254)
    birthday: date | None = None
    sex: CustomerGenderEnums | None = None
    phones: list[CustomerPhoneSchema] | None = None
    address: CustomerAddressSchema | None = None


class CustomerAddressReadSchema(BaseModel):
    id: int | None = None
    index: str | None = None
    country_iso: str | None = Field(None, validation_alias='countryIso')
    region: str | None = None
    city: str | None = None
    street: str | None = None
    building: str | None = None
    flat: str | None = None
    text: str | None = None


class CustomerReadSchema(BaseModel):
    id: int
    first_name: str | None = Field(None, validation_alias='firstName')
    last_name: str | None = Field(None, validation_alias='lastName')
    email: str | None = None
    sex: str | None = None
    birthday: date | None = None
    created_at: datetime = Field(validation_alias='createdAt')

    phones: list[CustomerPhoneSchema] = []
    address: CustomerAddressReadSchema | None = None


class CustomerListResponseSchema(BaseModel):
    pagination: PaginationSchema
    customers: list[CustomerReadSchema]
