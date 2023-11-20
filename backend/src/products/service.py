import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from fastapi import HTTPException, status
from typing import List

from .schemas import ProductCreate, ProductCreateDB
from .models import ProductModel
from ..database import async_session_maker
from .repository import ProductRepository


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
    async def update_product():
        pass
    
    @classmethod
    async def delete_product():
        pass
    
    @classmethod
    async def get_product_list():
        pass


