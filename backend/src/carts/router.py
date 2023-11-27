from fastapi import APIRouter, Depends
from src.carts.service import CartService
from src.users.dependencies import get_current_user

from src.users.models import UserModel


cart_router = APIRouter(prefix="/cart", tags=["carts"])


@cart_router.post("/create")
async def create_cart(user: UserModel = Depends(get_current_user)):
    return await CartService.create_cart(user_id=user.id)
