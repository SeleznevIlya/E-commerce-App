import uuid

from fastapi import HTTPException, status
from src.orders.models import PromoCodeModel
from src.carts.service import CartService

from src.orders.schemas import OrderCreate, Promocode, PromocodeCreate
from src.orders.repository import OrderRepository, PromocodeRepository

from ..database import async_session_maker

class OrderService:
    
    @classmethod
    async def create_new_order(cls, user_id: uuid.UUID, promocode: str = None):
        async with async_session_maker() as session:
            user_cart = await CartService.get_cart(user_id=user_id)

            if not user_cart.product_associations:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User cart is empty"
                )
            
            if promocode:
                try:
                    db_promocode = await PromocodeService.get_promocode(promocode=promocode)
                except HTTPException as e:
                    return {"details": "Incorrect promocode"}

                discount: str = db_promocode.discount
                total_discount = user_cart.total_amount * (discount/100)
                payment_amount = user_cart.total_amount - total_discount


            await OrderRepository.add(
                session,
                OrderCreate(
                    user_id=user_id,
                    promocode=promocode,
                    total_amount=user_cart.total_amount,
                    total_discount=int(total_discount),
                    payment_amount=int(payment_amount),
                )
            )
            await session.commit()
        
        # return {"details": "Cart creating is succesfully"}
        return user_cart.total_amount, int(total_discount), int(payment_amount)

    @classmethod
    async def get_all_orders(cls):
        pass

    @classmethod
    async def get_order_by_id(cls, order_id: uuid.UUID):
        pass

    @classmethod
    async def get_orders_by_user(cls, user_id: uuid.UUID):
        pass

    @classmethod
    async def update_order_status(cls, order_id: uuid.UUID):
        pass


class PromocodeService:
    
    @classmethod
    async def create_promocode(cls, promocode: str, discount: int) -> Promocode:
        async with async_session_maker() as session:
            promocode = await PromocodeRepository.add(
                session,
                PromocodeCreate(
                    promocode=promocode,
                    discount=discount
                )
            )
            await session.commit()
        
        return promocode

    @classmethod
    async def get_promocode(cls, promocode: str) -> PromoCodeModel:
        async with async_session_maker() as session:
            db_promocode = await PromocodeRepository.find_one_or_none(session, promocode=promocode)
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
