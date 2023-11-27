from src.repository import BaseRepository
from src.carts.models import CartModel
from src.carts.schemas import CartCreateDB, CartUpdate


class CartRepository(BaseRepository[CartModel, CartCreateDB, CartUpdate]):
    model = CartModel
    