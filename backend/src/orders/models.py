import uuid
import enum

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


if TYPE_CHECKING:
    from ..products.models import ProductModel


class OrderStatus(enum.Enum):
    PENDING = "pending"
    RECEIVED = "received"
    COMPLETED = "completed"
    CANCELED = "canceled"


class OrderProductModel(Base):
    __tablename__ = "order_product"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("product.id"))
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("order.id"))

    count: Mapped[int] = mapped_column(default=1, server_default="1")

    # association between OrderProduct -> Order

    order: Mapped["OrderModel"] = relationship(back_populates="product_associations")

    # association between OrderProduct -> Product

    product: Mapped["ProductModel"] = relationship(back_populates="order_associations")


class OrderModel(Base):
    __tablename__ = "order"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, index=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )
    total_amount: Mapped[int] = mapped_column(default=0)
    total_discount: Mapped[int] = mapped_column(default=0)
    payment_amount: Mapped[int] = mapped_column(default=0)
    is_paid: Mapped[bool] = mapped_column(default=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus, name="order_status"), server_default="PENDING")

    product_associations: Mapped[list["OrderProductModel"]] = relationship(back_populates="order")
