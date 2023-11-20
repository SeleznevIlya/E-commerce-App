from fastapi import APIRouter

from .service import ProductService
from .schemas import Product, ProductCreate


product_router = APIRouter(prefix="/product", tags=["product"])


@product_router.get("/{product_name}")
async def get_product(product_name: str):
    return await ProductService.get_product(product_name)


@product_router.get("/search/{partname}")
async def get_product_list_by_partname(partname: str):
    return await ProductService.get_product_list_by_partname(partname)


@product_router.post("/create")
async def create_product(product: ProductCreate) -> Product:
    return await ProductService.create_new_product(product)


@product_router.delete("/{product_name}")
async def delete_product(product_name: str):
    return await ProductService.delete_product(product_name)


async def update_product():
    pass


async def update_product_partial():
    pass