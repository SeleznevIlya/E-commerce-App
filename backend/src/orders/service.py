import uuid

from fastapi import HTTPException, status

from src.products.repository import ProductRepository
from src.orders.utils import count_total_discount_and_payment_amount
from src.orders.models import OrderModel, OrderProductModel, PromoCodeModel
from src.carts.service import CartService

from src.orders.schemas import (
    OrderCreate,
    OrderUpdate,
    OrderUpdateDB,
    Promocode,
    PromocodeCreate,
)
from src.orders.repository import OrderRepository, PromocodeRepository

from src.database import async_session_maker


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

            for product_in_cart in user_cart.product_associations:
                products_in_cart[str(product_in_cart.product.id)] = product_in_cart.count

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

                (
                    total_discount,
                    payment_amount,
                ) = count_total_discount_and_payment_amount(
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

        return new_order, products_in_cart

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

    @classmethod
    async def get_all_orders(cls):
        pass

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
        cls, user_id: uuid.UUID, offset: int = 0, limit: int = 100, **filter_by
    ) -> OrderModel:
        async with async_session_maker() as session:
            db_order = await OrderRepository.find_all_with_association_model(
                session,
                OrderProductModel.product,
                user_id=user_id,
                offset=offset,
                limit=limit,
                **filter_by,
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
    async def delete_promocode(cls):
        pass

    @classmethod
    async def update_promocode(cls):
        pass
