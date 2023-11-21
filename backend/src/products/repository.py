from src.repository import BaseRepository
from src.products.models import CategoryModel, ProductModel
from src.products.schemas import CategoryCreateDB, CategoryUpdateDB, ProductCreateDB, ProductUpdate


class ProductRepository(BaseRepository[ProductModel, ProductCreateDB, ProductUpdate]):
    model = ProductModel


class CategoryRepository(BaseRepository[CategoryModel, CategoryCreateDB, CategoryUpdateDB]):
    model = CategoryModel