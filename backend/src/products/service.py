import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from fastapi import HTTPException, status
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .schemas import CategoryCreate, CategoryCreateDB, ProductCreate, ProductCreateDB, ProductUpdate, ProductUpdateDB, ProductUpdatePartial
from .models import CategoryModel, ProductCategoryModel, ProductModel
from ..database import async_session_maker
from .repository import CategoryRepository, ProductRepository


class ProductService:
    
    @classmethod
    async def create_new_product(cls, product: ProductCreate) -> ProductModel:
        async with async_session_maker() as session:
            product_with_name_exist = await ProductRepository.find_one_or_none(
                session, 
                product_name=product.product_name,
                )
            if product_with_name_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Product with this product name already exists"
                )
            product_with_code_exist = await ProductRepository.find_one_or_none(
                session, 
                product_code=product.product_code,
                )
            if product_with_code_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Product with this product code already exists"
                )
            
            db_product = await ProductRepository.add(
                session,
                ProductCreateDB(
                    **product.model_dump()
                )
            )
            
            await session.commit()
        return db_product
    
    @classmethod
    async def get_product(cls, product_name: str) -> ProductModel:
        async with async_session_maker() as session:
            db_product = await ProductRepository.find_one_or_none(
                session, 
                product_name=product_name,
                )
        
        if db_product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return db_product
    
    @classmethod
    async def get_product_list(cls, *filter, offset: int = 0, limit: int = 100, **filter_by):
        async with async_session_maker() as session:
            products = await ProductRepository.find_all(
                session, 
                *filter, 
                offset=offset, 
                limit=limit, 
                **filter_by
                )
        
        if products is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Products not found"
            )
        return products
    
    @classmethod
    async def get_product_list_by_partname(cls, product_name: str) -> list[ProductModel]:
        async with async_session_maker() as session:
            products = await ProductRepository.find_all(
                session, 
                ProductModel.product_name.like(f'%{product_name}%')
                )
        
        if products is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Products not found"
            )
        return products
    
    @classmethod
    async def update_product(cls, query_product_name: str, product: ProductUpdate) -> ProductModel:
        async with async_session_maker() as session:
            db_product = await ProductRepository.find_one_or_none(session, 
                                                               ProductModel.product_name == query_product_name)
            if db_product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

            product_in = ProductUpdateDB(
                **product.model_dump()
            )

            product_update = await ProductRepository.update(
                session,
                ProductModel.product_name == query_product_name,
                obj_in=product_in,
            )

            await session.commit()
            
            return product_update
    

    # @classmethod
    # async def update_product_partial(cls, query_product_name: str, product: ProductUpdatePartial) -> ProductModel:
    #     async with async_session_maker() as session:
    #         db_product = await ProductRepository.find_one_or_none(session, 
    #                                                            ProductModel.product_name == query_product_name)
    #         if db_product is None:
    #             raise HTTPException(
    #                 status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    #         product_in = ProductUpdateDB(
    #             **product.model_dump()
    #         )

    #         product_update = await ProductRepository.update(
    #             session,
    #             ProductModel.product_name == query_product_name,
    #             obj_in=product_in,
    #         )

    #         await session.commit()
            
    #         return product_update
        
    
    @classmethod
    async def delete_product(cls, product_name: str):
        async with async_session_maker() as session:
            db_product = await ProductRepository.find_one_or_none(
                session, 
                product_name=product_name,
                )
    
            if db_product is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
                )
            
            await ProductRepository.delete(
                session,
                ProductModel.product_name == product_name,
            )
            await session.commit()

        return {'details': "Product deleted successfully"}
    
    @classmethod
    async def add_product_categories(cls, product_name: str, request_categories: list):
        async with async_session_maker() as session:
            product = await ProductRepository.find_one_with_connected_model(
                session,
                ProductModel.categories,
                product_name=product_name,
            )

            categories_list = []

            for category in request_categories:
                category_result = await CategoryRepository.find_one_or_none(
                session, 
                category_name=category,
                )
                if category_result:
                    categories_list.append(category_result)
            
            product.categories = categories_list

            await session.commit()        
    

class CategoryService:

    @classmethod
    async def create_new_category(cls, category: CategoryCreate) -> CategoryModel:
        async with async_session_maker() as session:
            category_exist = await CategoryRepository.find_one_or_none(
                session, 
                category_name=category.category_name,
                )
            if category_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Category with this category name already exists"
                )
            
            db_category = await CategoryRepository.add(
                session,
                CategoryCreateDB(
                    **category.model_dump()
                )
            )
            
            await session.commit()
        return db_category
    
    @classmethod
    async def update_category():
        pass
    
    @classmethod
    async def delete_category(cls, category_name: str):
        async with async_session_maker() as session:
            db_category = await CategoryRepository.find_one_or_none(
                session, 
                category_name=category_name,
                )
    
            if db_category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
                )
            
            await CategoryRepository.delete(
                session,
                CategoryModel.category_name == category_name,
            )
            await session.commit()

        return {'details': "Category deleted successfully"}
    