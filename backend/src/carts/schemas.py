import uuid

from typing import Optional
from pydantic import BaseModel, Field


class CartBase(BaseModel):
    
    user_id: Optional[uuid.UUID] = Field(None)
    total_amount: Optional[int] = Field(None)


class CartCreate(CartBase):
    pass


class CartCreateDB(CartBase):
    pass


class CartUpdate(BaseModel):
    pass


class CartUpdateDB(CartBase):
    pass


class ProductInCart(BaseModel):
    id: uuid.UUID
    product_name: str
    description: str
    cost: int
    count: int
    rating: int


class Products(BaseModel):
    count: int
    product: ProductInCart

    
class Cart(CartBase):
    id: uuid.UUID
    user_id: uuid.UUID
    total_amount: int = 0
    product_associations: list[Products]
    


    class Config:
        from_attributes = True