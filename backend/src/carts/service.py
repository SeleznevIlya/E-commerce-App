import uuid
from fastapi import HTTPException, status

from .schemas import CartCreate, CartCreateDB, CartUpdate, CartUpdateDB
from .models import CartModel, CartProductModel
from .repository import CartRepository
from ..database import async_session_maker


class CartService:
    
    @classmethod
    async def create_cart(cls, user_id: uuid.UUID):
        async with async_session_maker() as session:
            await CartRepository.add(
                session,
                CartCreate(
                    user_id=user_id,
                    total_amount=0
                )
            )
            await session.commit()
        
        return {"details": "Cart creating is succesfully"}


    @classmethod
    async def get_cart(cls):
        pass

    @classmethod
    async def add_product_in_cart(cls):
        pass

    @classmethod
    async def remove_product_from_cart(cls):
        pass

