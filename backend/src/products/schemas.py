import uuid
from typing import Optional

from pydantic import BaseModel, Field


class ProductBase(BaseModel):

    product_name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    product_code:  Optional[str] = Field(None)
    cost:  Optional[int] = Field(None)
    rating:  Optional[int] = Field(None)


class ProductCreate(ProductBase):
    product_name: str
    product_code: str
    description: str
    count: int


class ProductCreateDB(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductUpdatePartial(ProductCreate):
    product_name: str | None = None
    product_code: str | None = None
    description: str | None = None
    cost: int | None = None
    count: int | None = None
    rating: int | None = None
    


class Product(ProductBase):
    id: uuid.UUID
    product_name: str
    description: str
    cost: int
    count: int
    rating: int


    class Config:
        from_attributes = True
