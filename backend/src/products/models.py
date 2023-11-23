from typing import Optional
import uuid
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.database import Base


class ProductCategoryModel(Base):
    __tablename__ = "product_category"

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), primary_key=True)

    # association between ProductCategory -> Product

    # product: Mapped["ProductModel"] = relationship(back_populates="category_associations")

    # association between ProductCategory -> Category

    # category: Mapped["CategoryModel"] = relationship(back_populates="product_associations")


class ProductModel(Base):
    __tablename__ = "product"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, index=True, default=uuid.uuid4)
    product_name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    product_code: Mapped[str]
    cost: Mapped[int] 
    count: Mapped[int] = mapped_column(default=0)
    rating: Mapped[int] = mapped_column(default=0)

    # many-to-many relationship to Category, bypassing the `ProductCategory` class

    categories: Mapped[list["CategoryModel"]] = relationship(
        secondary="product_category", back_populates="products"
    )

    # association between Product -> ProductCategory -> Category

    # category_associations: Mapped[list["ProductCategoryModel"]] = relationship(back_populates="product")


    def __repr__(self) -> str:
        return f'ProductModel: product name = {self.product_name}'


class CategoryModel(Base):
    __tablename__ = "category"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, index=True, default=uuid.uuid4)
    category_name: Mapped[str] = mapped_column(String(30))

    # many-to-many relationship to Product, bypassing the `ProductCategory` class

    products: Mapped[list["ProductModel"]] = relationship(
        secondary="product_category", back_populates="categories"
    )

    # association between Category -> ProductCategory -> Product
    
    # product_associations: Mapped[list["ProductCategoryModel"]] = relationship(back_populates="category")

    

# class ProductImage(Base):
#     __tablename__ = "product_image"
    
#     image_name: Mapped[str] = mapped_column(String(50), primary_key=True)
#     image_path: Mapped[str]
#     filetype: Mapped[str]

#     product_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("product.id", ondelete="CASCADE"))
