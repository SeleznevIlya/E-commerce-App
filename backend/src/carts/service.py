import uuid
from fastapi import HTTPException, status
from sqlalchemy import delete

from ..products.repository import ProductRepository

from .schemas import CartCreate, CartCreateDB, CartUpdate, CartUpdateDB
from .models import CartModel, CartProductModel
from .repository import CartProductRepository, CartRepository
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
    async def get_cart(cls, user_id: uuid.UUID) -> CartModel:
        async with async_session_maker() as session:
            db_cart = await CartRepository.find_one_with_association_model(
                session,
                CartProductModel.product,
                user_id=user_id
            )
        
        return db_cart

    @classmethod
    async def add_product_in_cart(cls, user_id: uuid.UUID, product_id: uuid.UUID):
        async with async_session_maker() as session:
            cart = await CartRepository.find_one_with_association_model(
                session,
                CartProductModel.product,
                user_id=user_id
            )

            product_result = await ProductRepository.find_one_or_none(
                session,
                id = product_id
            )

            if product_result:
                for obj in cart.product_associations:
                    if str(obj.product_id) == product_id:
                        obj.count += 1
                        break
                else:
                    associate_model = CartProductModel(product=product_result)
                
                    cart.product_associations.append(
                        associate_model
                    )

                cart.total_amount += product_result.cost
            
            await session.commit()
        return {"status": 200}

    @classmethod
    async def remove_all_products_from_cart(cls, user_id: uuid.UUID):
        async with async_session_maker() as session:
            cart = await CartRepository.find_one_with_association_model(
                session,
                CartProductModel.product,
                user_id=user_id
            )

            cart.total_amount = 0

            await CartProductRepository.delete(
                session,
                CartProductModel.cart_id == cart.id
                )

            await session.commit()
        return {"details": "Cart is empty"}
    
    @classmethod
    async def remove_product_from_cart(cls, user_id: uuid.UUID, product_id: uuid.UUID):
        async with async_session_maker() as session:
            cart = await CartRepository.find_one_with_association_model(
                session,
                CartProductModel.product,
                user_id=user_id
            )

            for obj in cart.product_associations:
                if str(obj.product_id) != product_id:
                    continue
                if obj.count == 1:
                    await CartProductRepository.delete(
                        session,
                        CartProductModel.product_id == product_id
                        )
                    cart.total_amount -= obj.product.cost
                elif obj.count > 1:
                    cart.total_amount -= obj.product.cost
                    obj.count -= 1
                    break

            await session.commit()



