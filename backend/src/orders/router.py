from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.carts.service import CartService
from src.orders.schemas import Order, OrderUpdate, Promocode, PromocodeUpdate
from src.orders.service import OrderService, PromocodeService
from src.tasks.service import send_message
from src.users.dependencies import get_current_superuser, get_current_user
from src.users.models import UserModel

order_router = APIRouter(prefix="/order", tags=["orders"])
promocode_router = APIRouter(prefix="/promocode", tags=["promocodes"])


@order_router.post("/")
async def create_order(
    promocode: str = None, user: UserModel = Depends(get_current_user)
):
    order, product_dict, product_dict_with_name = await OrderService.create_new_order(
        user_id=user.id, promocode=promocode
    )
    send_message.delay(
        "order",
        order_id=order.id,
        product_dict=product_dict_with_name,
        email_to=user.email,
    )
    await OrderService.add_products_in_order(product_dict, order.id)
    await CartService.remove_all_products_from_cart(user_id=user.id)
    return {
        "status": 200,
        "details": "Your order has beed created",
        "order_id": order.id,
    }


@order_router.get("/")
async def get_all_orders(
    offset: Optional[int] = 0,
    limit: Optional[int] = 100,
    user: UserModel = Depends(get_current_superuser),
) -> list[Order]:
    return await OrderService.get_orders_by_user(offset=offset, limit=limit)


@order_router.get("/me")
@cache(expire=30)
async def get_my_orders(
    offset: Optional[int] = 0,
    limit: Optional[int] = 100,
    user: UserModel = Depends(get_current_user),
) -> list[Order]:
    return await OrderService.get_orders_by_user(
        offset=offset, limit=limit, user_id=user.id
    )


@order_router.get("/{order_id}/details")
async def get_order_by_id(
    order_id: str, user: UserModel = Depends(get_current_user)
) -> Order:
    order = await OrderService.get_order_by_id(order_id=order_id)
    return order


@order_router.get("/{user_id}")
@cache(expire=30)
async def get_orders_by_user(
    user_id: str, user: UserModel = Depends(get_current_superuser)
) -> list[Order]:
    return await OrderService.get_orders_by_user(user_id=user_id)


@order_router.patch("/")
async def update_order_status_by_id(order: OrderUpdate, order_id: str):
    return await OrderService.update_order_status(order=order, order_id=order_id)


@promocode_router.post("/")
async def create_promocode(promocode: str, discount: int):
    return await PromocodeService.create_promocode(
        promocode=promocode, discount=discount
    )


@promocode_router.get("/{promocode}")
@cache(expire=30)
async def get_promocode(promocode: str):
    return await PromocodeService.get_promocode(promocode=promocode)


@promocode_router.get("/")
async def get_promocode_list(
    offset: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> list[Promocode]:
    return await PromocodeService.get_promocode_list(offset=offset, limit=limit)


@promocode_router.delete("/delete")
async def delete_promocode(promocode: str):
    return await PromocodeService.delete_promocode(promocode)


@promocode_router.put("/{query_promocode}")
async def update_promocode(
    query_promocode: str, promocode: PromocodeUpdate
) -> Promocode:
    return await PromocodeService.update_promocode(
        query_promocode=query_promocode, promocode=promocode
    )
