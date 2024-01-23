import uuid
from typing import Optional

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    category_name: Optional[str] = Field(None)


class CategoryCreate(CategoryBase):
    category_name: str


class CategoryCreateDB(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryUpdateDB(CategoryBase):
    pass


class Category(CategoryBase):
    id: uuid.UUID
    category_name: str

    class Config:
        from_attributes = True


# _________________________________


class ProductBase(BaseModel):
    product_name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    product_code: Optional[str] = Field(None)
    cost: Optional[int] = Field(None)
    rating: Optional[int] = Field(None)
    count: Optional[int] = Field(None)


class ProductCreate(ProductBase):
    product_name: str
    product_code: str
    description: str
    count: int
    cost: int


class ProductCreateDB(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_name: str
    product_code: str
    description: str
    count: int
    cost: int


class ProductUpdateDB(ProductBase):
    pass


# class ProductUpdatePartial(ProductUpdate):
#     product_name: str | None = None
#     product_code: str | None = None
#     description: str | None = None
#     cost: int | None = None
#     count: int | None = None


class Product(ProductBase):
    id: uuid.UUID
    product_name: str
    description: str
    cost: int
    count: int
    rating: int
    categories: list[Category]

    class Config:
        from_attributes = True
