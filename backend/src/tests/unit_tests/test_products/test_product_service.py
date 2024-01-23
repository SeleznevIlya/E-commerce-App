from fastapi import HTTPException
import pytest

from src.products.service import CategoryService, ProductService
from src.products.schemas import ProductCreate, CategoryCreate


class TestProduct:
    
    @pytest.mark.parametrize('product_name, product_code, description, count, cost, rating', [
        ("Pandemic-World-of-Warcraft", "ZT4021RU", "My favorite board game", 0, 5490, 1),
        ]
    )
    async def test_create_product(self, product_name, product_code, description, count, cost, rating):
        product_schema = ProductCreate(
            product_name=product_name,
            product_code=product_code,
            description=description,
            count=count,
            cost=cost,
            rating=rating
        )
        new_product = await ProductService.create_new_product(product_schema)

        assert new_product.product_name == product_name

    @pytest.mark.parametrize('category_name', [
        ("Test Category1"),
        ("Test Category2"),
        ("Test Category3"),
        ]
    )
    async def test_create_new_category(self, category_name: str):
        category_schema = CategoryCreate(category_name=category_name)
        test_category = await CategoryService.create_new_category(category_schema)
        assert test_category.category_name == category_name

    @pytest.mark.parametrize('product_name, category_list', [
            ("Pandemic-World-of-Warcraft", ["Test Category1", "Test Category2"]),
           
            ]
        )
    async def test_add_product_categories(self, product_name, category_list):
        res = await ProductService.add_product_categories(product_name, category_list)

        print(res.categories)

    @pytest.mark.parametrize('product_name, exists', [
        ("Pandemic-World-of-Warcraft", True),
        ("123", True),
        ("qwe", False),
        ]
    )
    async def test_get_product(self, product_name, exists):
        try:
            test_product = await ProductService.get_product(product_name=product_name)
            assert test_product.product_name == product_name
        except HTTPException:
            assert exists == False

    @pytest.mark.parametrize('product_name', [
        ("Pandemic-World-of-Warcraft"),
        ]
    )
    async def test_delete_product(self, product_name):
        res = await ProductService.delete_product(product_name)
        
        assert res["details"] == "Product deleted successfully" 
