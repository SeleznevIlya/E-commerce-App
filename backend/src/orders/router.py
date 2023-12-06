from fastapi import APIRouter, Depends
from src.orders.schemas import Order
from src.carts.service import CartService

from src.orders.service import OrderService, PromocodeService

from src.users.dependencies import get_current_user, get_current_superuser
from src.users.models import UserModel


order_router = APIRouter(prefix="/order", tags=["orders"])
promocode_router = APIRouter(prefix="/promocode", tags=["promocodes"])


@order_router.post("/")
async def create_order(promocode: str = None, user: UserModel = Depends(get_current_user)):
    order, product_dict = await OrderService.create_new_order(user_id=user.id, promocode=promocode)
    await OrderService.add_products_in_order(product_dict, order.id)
    await CartService.remove_all_products_from_cart(user_id=user.id)
    return {"status": 200, "details": "Your order has beed created"}, order

@order_router.get("/")
async def get_all_orders(user: UserModel = Depends(get_current_superuser)):
    pass

@order_router.get("/me")
async def get_my_orders(user: UserModel = Depends(get_current_user)) -> list[Order]:
    return await OrderService.get_orders_by_user(user_id=user.id)

@order_router.get("/{order_id}/details")
async def get_order_by_id(order_id: str, user: UserModel = Depends(get_current_superuser)) -> Order:
    order = await OrderService.get_order_by_id(order_id=order_id)
    return order

@order_router.get("/{user_id}")
async def get_orders_by_user(user_id: str, user: UserModel = Depends(get_current_superuser)) -> list[Order]:
    return await OrderService.get_orders_by_user(user_id=user_id)

@promocode_router.post("/")
async def create_promocode(promocode: str, discount: int):
    return await PromocodeService.create_promocode(promocode=promocode, discount=discount)

@promocode_router.get("/{promocode}")
async def get_promocode(promocode:str):
    return await PromocodeService.get_promocode(promocode=promocode)