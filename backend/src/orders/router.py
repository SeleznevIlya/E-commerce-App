from fastapi import APIRouter, Depends

from src.users.dependencies import get_current_user, get_current_superuser
from src.users.models import UserModel


order_router = APIRouter(prefix="/order", tags=["orders"])


@order_router.post("/")
async def create_order(user: UserModel = Depends(get_current_user)):
    pass

@order_router.get("/")
async def get_all_orders(user: UserModel = Depends(get_current_superuser)):
    pass

@order_router.get("/")
async def get_orders_by_user(user: UserModel = Depends(get_current_user)):
    pass

@order_router.get("/")
async def get_order_by_id(order_id: str, user: UserModel = Depends(get_current_superuser)):
    pass
