from fastapi import APIRouter, Depends
from src.carts.service import CartService
from src.users.dependencies import get_current_user

from src.users.models import UserModel


cart_router = APIRouter(prefix="/cart", tags=["carts"])


# @cart_router.post("/create")
# async def create_cart(user: UserModel = Depends(get_current_user)):
#     return await CartService.create_cart(user_id=user.id)


@cart_router.get("/")
async def get_cart(user: UserModel = Depends(get_current_user)):
    return await CartService.get_cart(user_id=user.id)


@cart_router.patch("/add_product")
async def add_product_in_cart(product_id: str, user: UserModel = Depends(get_current_user)):
    return await CartService.add_product_in_cart(user_id=user.id, product_id=product_id)


@cart_router.patch("/clear")
async def remove_all_products_from_cart(user: UserModel = Depends(get_current_user)):
    return await CartService.remove_all_products_from_cart(user_id=user.id)

