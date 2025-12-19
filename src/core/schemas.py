from typing import Literal

from pydantic import BaseModel, Field


class MessageResponseSchema(BaseModel):
    message: str
    id: int


class PaginationSchema(BaseModel):
    limit: int
    total_count: int = Field(validation_alias='totalCount')
    current_page: int = Field(validation_alias='currentPage')
    total_page_count: int = Field(validation_alias='totalPageCount')


class BaseFilter(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: Literal['20', '50', '100'] = '20'
