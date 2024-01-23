import uuid

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    created_at: Optional[datetime] = Field(None)
    total_amount: Optional[int] = Field(None)
    total_discount: Optional[int] = Field(None)
    payment_amount: Optional[int] = Field(None)
    is_paid: bool = Field(False)
    promocode: Optional[str] = Field(None)
    status: Optional[str] = Field(None)


class OrderCreate(OrderBase):
    user_id: uuid.UUID
    total_amount: int
    total_discount: int
    payment_amount: int
    promocode: Optional[str]


class OrderCreateDB(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Literal["PENDING", "RECEIVED", "COMPLETED", "CANCELED"]


class OrderUpdateDB(OrderBase):
    pass


class ProductInOrder(BaseModel):
    id: uuid.UUID
    product_name: str
    description: str
    cost: int
    count: int
    rating: int


class Products(BaseModel):
    count: int
    product: ProductInOrder


class Order(OrderBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    total_amount: int
    total_discount: int
    payment_amount: int
    is_paid: bool
    promocode: str | None
    status: str

    product_associations: list[Products]

    class Config:
        from_attributes = True


# _________________________________


class PromocodeBase(BaseModel):
    promocode: Optional[str] = Field(None)
    discount: Optional[int] = Field(None)


class PromocodeCreate(PromocodeBase):
    promocode: str
    discount: int


class PromocodeCreateDB(PromocodeBase):
    pass


class PromocodeUpdate(BaseModel):
    discount: int


class PromocodeUpdateDB(PromocodeBase):
    pass


class Promocode(PromocodeBase):
    id: uuid.UUID
    promocode: str
    discount: int

    class Config:
        from_attributes = True
