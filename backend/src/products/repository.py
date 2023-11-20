from src.repository import BaseRepository
from src.products.models import ProductModel
from src.products.schemas import ProductCreate, ProductUpdate


class ProductRepository(BaseRepository[ProductModel, ProductCreate, ProductUpdate]):
    model = ProductModel