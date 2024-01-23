import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from ..products.models import ProductModel
    from ..users.models import UserModel


class CartProductModel(Base):
    __tablename__ = "cart_product"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    product_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("product.id", ondelete="CASCADE")
    )
    cart_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cart.id", ondelete="CASCADE")
    )

    count: Mapped[int] = mapped_column(default=1, server_default="1")

    # association between CartProduct -> Cart

    cart: Mapped["CartModel"] = relationship(back_populates="product_associations")

    # association between CartProduct -> Product

    product: Mapped["ProductModel"] = relationship(back_populates="cart_associations")


class CartModel(Base):
    __tablename__ = "cart"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, index=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), unique=True
    )
    total_amount: Mapped[int] = mapped_column(default=0)

    # product_list: Mapped[list["ProductModel"]] = relationship(
    #     secondary="cart_product", back_populates="carts"
    # )

    user: Mapped["UserModel"] = relationship(back_populates="cart")

    product_associations: Mapped[list["CartProductModel"]] = relationship(
        back_populates="cart"
    )

    def __str__(self) -> str:
        return f"User's cart: {self.user_id}"
