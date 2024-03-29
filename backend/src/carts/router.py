from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.carts.schemas import Cart
from src.carts.service import CartService
from src.users.dependencies import get_current_user
from src.users.models import UserModel

cart_router = APIRouter(prefix="/cart", tags=["carts"])


@cart_router.get("/")
@cache(expire=30)
async def get_cart(user: UserModel = Depends(get_current_user)) -> Cart:
    return await CartService.get_cart(user_id=user.id)


@cart_router.patch("/add_product")
async def add_product_in_cart(
    product_id: str, user: UserModel = Depends(get_current_user)
):
    return await CartService.add_product_in_cart(user_id=user.id, product_id=product_id)


@cart_router.patch("/clear")
async def remove_all_products_from_cart(user: UserModel = Depends(get_current_user)):
    return await CartService.remove_all_products_from_cart(user_id=user.id)


@cart_router.patch("/remove_product")
async def remove_product_from_cart(
    product_id: str, user: UserModel = Depends(get_current_user)
):
    return await CartService.remove_product_from_cart(
        user_id=user.id, product_id=product_id
    )
