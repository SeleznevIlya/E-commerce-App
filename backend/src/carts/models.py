from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


if TYPE_CHECKING:
    from ..users.models import UserModel
    from ..products.models import ProductModel


class CartProductModel(Base):
    __tablename__ = "cart_product"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id"))

    count: Mapped[int] = mapped_column(default=1, server_default="1")



class CartModel(Base):
    __tablename__ = "cart"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, index=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    total_amount: Mapped[int] = mapped_column(default=0)

    product_list: Mapped[list["ProductModel"]] = relationship(
        secondary="cart_product", back_populates="carts"
    )
    
    user: Mapped['UserModel'] = relationship(back_populates="cart")
