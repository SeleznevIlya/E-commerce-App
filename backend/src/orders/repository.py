from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.orders.models import OrderModel, PromoCodeModel
from src.orders.schemas import (
    OrderCreateDB,
    OrderUpdate,
    PromocodeCreateDB,
    PromocodeUpdate,
)
from src.repository import BaseRepository


class OrderRepository(BaseRepository[OrderModel, OrderCreateDB, OrderUpdate]):
    model = OrderModel

    @classmethod
    async def find_one_with_association_model(
        cls, session: AsyncSession, association_model, **filter_by
    ) -> Optional[OrderModel]:
        stmt = (
            select(cls.model)
            .filter_by(**filter_by)
            .options(
                selectinload(cls.model.product_associations).joinedload(
                    association_model
                )
            )
        )
        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def find_all_with_association_model(
        cls,
        session: AsyncSession,
        association_model,
        *filter,
        offset: int = 0,
        limit: int = 100,
        **filter_by,
    ) -> list[OrderModel]:
        stmt = (
            select(cls.model)
            .filter_by(**filter_by)
            .options(
                selectinload(cls.model.product_associations).joinedload(
                    association_model
                )
            )
            .offset(offset)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()


class PromocodeRepository(
    BaseRepository[PromoCodeModel, PromocodeCreateDB, PromocodeUpdate]
):
    model = PromoCodeModel
