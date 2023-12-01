import uuid

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    created_at: Optional[date] = Field(None)
    total_amount: Optional[int] = Field(None)
    total_discount: Optional[int] = Field(None)
    payment_amount: Optional[int] = Field(None)
    is_paid: bool = Field(False)
    status: Optional[str] = Field(None)
    

class OrderCreate(OrderBase):
    total_amount: int
    total_discount: int
    payment_amount: int


class OrderCreateDB(OrderBase):
    pass


class OrderUpdate(BaseModel):
    pass


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
    created_at: date
    total_amount: int
    total_discount: int
    payment_amount: int
    is_paid: bool
    status: str

    product_associations: list[Products]
    

    class Config:
        from_attributes = True