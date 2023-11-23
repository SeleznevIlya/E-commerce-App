from typing import Annotated, Optional
from fastapi import APIRouter, Query

from .service import CategoryService, ProductService
from .schemas import Category, CategoryCreate, Product, ProductCreate, ProductUpdate, ProductUpdatePartial


product_router = APIRouter(prefix="/product", tags=["product"])


@product_router.post("/create")
async def create_product(product: ProductCreate, q: Annotated[list[str], Query()] = []) -> Product:
    result = await ProductService.create_new_product(product)
    await ProductService.add_product_categories(result.product_name, q)
    return result



@product_router.get("/{product_name}")
async def get_product(product_name: str) -> Product:
    return await ProductService.get_product(product_name)


@product_router.get("/")
async def get_product_list(offset: Optional[int] = 0,
                           limit: Optional[int] = 100,
                           ) -> list[Product]:
    return await ProductService.get_product_list(offset=offset, limit=limit)


@product_router.get("/search/{partname}")
async def get_product_list_by_partname(partname: str) -> list[Product]:
    return await ProductService.get_product_list_by_partname(partname)


@product_router.put("/{product_name}")
async def update_product(product_name: str, product: ProductUpdate) -> Product:
    return await ProductService.update_product(product_name, product)


# @product_router.patch("/{product_name}")
# async def update_product_partial(product_name: str, product: ProductUpdatePartial):
#     return await ProductService.update_product_partial(product_name, product)


@product_router.delete("/{product_name}")
async def delete_product(product_name: str):
    return await ProductService.delete_product(product_name)


@product_router.post("/category/create")
async def create_category(category: CategoryCreate) -> Category:
    return await CategoryService.create_new_category(category)


@product_router.delete("/category/delete")
async def delete_category(category_name: str):
    return await CategoryService.delete_category(category_name)
