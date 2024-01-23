import uuid

from fastapi import HTTPException, status

from src.carts.service import CartService
from src.database import async_session_maker
from src.orders.models import OrderModel, OrderProductModel, PromoCodeModel
from src.orders.repository import OrderRepository, PromocodeRepository
from src.orders.schemas import (
    OrderCreate,
    OrderUpdate,
    OrderUpdateDB,
    Promocode,
    PromocodeCreate,
    PromocodeUpdate,
    PromocodeUpdateDB,
)
from src.orders.utils import count_total_discount_and_payment_amount
from src.products.repository import ProductRepository


class OrderService:
    @classmethod
    async def create_new_order(cls, user_id: uuid.UUID, promocode: str = None):
        async with async_session_maker() as session:
            user_cart = await CartService.get_cart(user_id=user_id)

            if not user_cart.product_associations:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User cart is empty"
                )

            products_in_cart = {}
            products_in_cart_with_name = {}

            for product_in_cart in user_cart.product_associations:
                products_in_cart[str(product_in_cart.product.id)] = product_in_cart.count
                products_in_cart_with_name[str(product_in_cart.product.id)] = [
                    product_in_cart.product.product_name,
                    product_in_cart.count,
                ]

            if promocode:
                try:
                    db_promocode = await PromocodeService.get_promocode(
                        promocode=promocode
                    )
                except HTTPException:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Incorrect promocode",
                    )

                total_discount, payment_amount = count_total_discount_and_payment_amount(
                    db_promocode.discount, user_cart.total_amount
                    )
            else:
                total_discount = 0
                payment_amount = user_cart.total_amount
                promocode = ""

            new_order = await OrderRepository.add(
                session,
                OrderCreate(
                    user_id=user_id,
                    promocode=promocode,
                    total_amount=user_cart.total_amount,
                    total_discount=int(total_discount),
                    payment_amount=int(payment_amount),
                ),
            )
            await session.commit()

        return new_order, products_in_cart, products_in_cart_with_name

    @classmethod
    async def add_products_in_order(cls, product_dict: dict, order_id: uuid.UUID):
        async with async_session_maker() as session:
            order = await OrderRepository.find_one_with_association_model(
                session, OrderProductModel.product, id=order_id
            )

            for product_id, count in product_dict.items():
                product_result = await ProductRepository.find_one_or_none(
                    session, id=product_id
                )

                associate_model = OrderProductModel(product=product_result, count=count)
                order.product_associations.append(associate_model)
            await session.commit()
        return {"status": 200}

    @classmethod
    async def get_all_orders(cls, offset: int = 0, limit: int = 100, **filter_by):
        async with async_session_maker() as session:
            orders = await OrderRepository.find_all(
                session, offset=offset, limit=limit, **filter_by
            )

        if orders is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Orders not found"
            )
        return orders

    @classmethod
    async def get_order_by_id(cls, order_id: uuid.UUID) -> OrderModel:
        async with async_session_maker() as session:
            db_order = await OrderRepository.find_one_with_association_model(
                session,
                OrderProductModel.product,
                id=order_id,
            )

            if db_order is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
                )
            return db_order

    @classmethod
    async def get_orders_by_user(
        cls, offset: int = 0, limit: int = 100, **filter_by
    ) -> list[OrderModel]:
        async with async_session_maker() as session:
            db_order = await OrderRepository.find_all_with_association_model(
                session,
                OrderProductModel.product,
                # user_id=user_id,
                offset=offset,
                limit=limit,
                **filter_by,
            )
            if db_order is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="You don't have any orders yet",
                )

        return db_order

    @classmethod
    async def update_order_status(cls, order: OrderUpdate, order_id: uuid.UUID):
        async with async_session_maker() as session:
            db_order = await OrderRepository.find_one_with_association_model(
                session,
                OrderProductModel.product,
                id=order_id,
            )

            if db_order is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
                )

            order_in = OrderUpdateDB(**order.model_dump())

            await OrderRepository.update(
                session,
                OrderModel.id == order_id,
                obj_in=order_in,
            )

            await session.commit()

        return {"status": 200, "details": f"Order status: {order.status}"}


class PromocodeService:
    @classmethod
    async def create_promocode(cls, promocode: str, discount: int) -> Promocode:
        async with async_session_maker() as session:
            db_promocode = await PromocodeRepository.find_one_or_none(
                session, promocode=promocode
            )
            if db_promocode:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Promocode already exists",
                )

            promocode = await PromocodeRepository.add(
                session, PromocodeCreate(promocode=promocode, discount=discount)
            )
            await session.commit()

        return promocode

    @classmethod
    async def get_promocode(cls, promocode: str) -> PromoCodeModel:
        async with async_session_maker() as session:
            db_promocode = await PromocodeRepository.find_one_or_none(
                session, promocode=promocode
            )
        if db_promocode is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Promocode not found"
            )
        return db_promocode

    @classmethod
    async def get_promocode_list(
        cls, offset: int = 0, limit: int = 100, **filter_by
    ) -> list[Promocode]:
        async with async_session_maker() as session:
            promocodes = await PromocodeRepository.find_all(
                session, offset=offset, limit=limit, **filter_by
            )

        if promocodes is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Promocodes not found"
            )
        return promocodes

    @classmethod
    async def delete_promocode(cls, promocode: str):
        async with async_session_maker() as session:
            db_promocode = await PromocodeRepository.find_one_or_none(
                session,
                promocode=promocode,
            )

            if db_promocode is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Promocode not found"
                )

            await PromocodeRepository.delete(
                session,
                PromoCodeModel.promocode == promocode,
            )
            await session.commit()

        return {"details": "Product deleted successfully"}

    @classmethod
    async def update_promocode(
        cls, query_promocode: str, promocode: PromocodeUpdate
    ) -> PromoCodeModel:
        async with async_session_maker() as session:
            db_promocode = await PromocodeRepository.find_one_or_none(
                session, PromoCodeModel.promocode == query_promocode
            )
            if db_promocode is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Promocode not found"
                )

            promocode_in = PromocodeUpdateDB(**promocode.model_dump())

            promocode_update = await PromocodeRepository.update(
                session,
                PromoCodeModel.promocode == query_promocode,
                obj_in=promocode_in,
            )

            await session.commit()

        return promocode_update
