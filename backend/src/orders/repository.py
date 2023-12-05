from src.repository import BaseRepository
from src.orders.models import OrderModel, PromoCodeModel
from src.orders.schemas import OrderCreateDB, OrderUpdate, PromocodeCreateDB, PromocodeUpdate


class OrderRepository(BaseRepository[OrderModel, OrderCreateDB, OrderUpdate]):
    model = OrderModel


class PromocodeRepository(BaseRepository[PromoCodeModel, PromocodeCreateDB, PromocodeUpdate]):
    model = PromoCodeModel