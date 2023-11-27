import uuid

from typing import Optional
from pydantic import BaseModel, Field

from ..products.schemas import Product


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

    
class Cart(CartBase):
    id: uuid.UUID
    user_id: uuid.UUID
    total_amount: int = 0
    products: list[Product]


    class Config:
        from_attributes = True