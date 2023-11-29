from typing import Optional
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository import BaseRepository
from src.carts.models import CartModel, CartProductModel
from src.carts.schemas import CartCreateDB, CartUpdate


class CartRepository(BaseRepository[CartModel, CartCreateDB, CartUpdate]):
    model = CartModel
    
    @classmethod
    async def find_one_with_association_model(cls, session: AsyncSession, association_model, **filter_by) -> Optional[CartModel]:
        stmt = (
            select(cls.model).
            filter_by(**filter_by).
            options(selectinload(cls.model.product_associations).
                    joinedload(association_model))
            )
        result = await session.execute(stmt)
        return result.scalar()
    

class CartProductRepository(BaseRepository[CartProductModel, None, None]):
    model = CartProductModel
