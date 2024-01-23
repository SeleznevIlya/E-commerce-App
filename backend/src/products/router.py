from typing import Annotated, Optional

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from .schemas import Category, CategoryCreate, Product, ProductCreate, ProductUpdate
from .service import CategoryService, ProductService

product_router = APIRouter(prefix="/product", tags=["product"])


@product_router.post("/create")
async def create_product(
    product: ProductCreate, category_list: Annotated[list[str], Query()] = []
) -> Product:
    new_product = await ProductService.create_new_product(product)
    res = await ProductService.add_product_categories(
        new_product.product_name, category_list
    )
    return res


@product_router.get("/{product_name}")
async def get_product(product_name: str) -> Product:
    return await ProductService.get_product(product_name)


@product_router.get("/")
@cache(expire=30)
async def get_product_list(
    offset: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> list[Product]:
    return await ProductService.get_product_list(offset=offset, limit=limit)


@product_router.get("/search/{partname}")
async def get_product_list_by_partname(partname: str) -> list[Product]:
    return await ProductService.get_product_list_by_partname(partname)


@product_router.put("/{product_name}")
async def update_product(product_name: str, product: ProductUpdate) -> ProductUpdate:
    return await ProductService.update_product(product_name, product)


@product_router.delete("/{product_name}")
async def delete_product(product_name: str):
    return await ProductService.delete_product(product_name)


@product_router.post("/category/create")
async def create_category(category: CategoryCreate) -> Category:
    return await CategoryService.create_new_category(category)


@product_router.get("/category/")
async def get_category_list(
    offset: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> list[Category]:
    return await CategoryService.get_category_list(offset=offset, limit=limit)


@product_router.delete("/category/delete")
async def delete_category(category_name: str):
    return await CategoryService.delete_category(category_name)
