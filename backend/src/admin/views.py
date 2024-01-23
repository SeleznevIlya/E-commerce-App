from sqladmin import ModelView

from src.carts.models import CartModel, CartProductModel
from src.orders.models import OrderModel, OrderProductModel
from src.products.models import CategoryModel, ProductModel
from src.users.models import UserModel


class UserAdmin(ModelView, model=UserModel):
    column_list = [
        UserModel.id,
        UserModel.email,
        UserModel.cart,
        UserModel.order,
    ]
    column_details_exclude_list = [UserModel.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class CartAdmin(ModelView, model=CartModel):
    column_list = [CartModel.id, CartModel.product_associations]
    can_delete = False
    name = "Корзина"
    name_plural = "Корзины"
    icon = "fa-solid fa-cart"


class CartProductAdmin(ModelView, model=CartProductModel):
    column_list = [
        CartProductModel.id,
        CartProductModel.product_id,
        CartProductModel.cart_id,
    ]
    can_delete = False
    name = "Корзина и продукты"
    name_plural = "Корзины и продукты"
    icon = "fa-solid fa-cart"


class ProductAdmin(ModelView, model=ProductModel):
    column_list = [
        ProductModel.id,
        ProductModel.categories,
        ProductModel.cost,
        ProductModel.count,
        ProductModel.description,
        ProductModel.product_code,
    ]
    name = "Продукт"
    name_plural = "Продукты"
    icon = "fa-solid fa-product"


class CategoryAdmin(ModelView, model=CategoryModel):
    column_list = [CategoryModel.id, CategoryModel.category_name]
    name = "Категория"
    name_plural = "Категории"
    icon = "fa-solid fa-product"


class OrderAdmin(ModelView, model=OrderModel):
    column_list = [
        OrderModel.id,
        OrderModel.created_at,
        OrderModel.is_paid,
        OrderModel.payment_amount,
        OrderModel.user,
        OrderModel.product_associations,
    ]
    can_delete = False
    name = "Заказ"
    name_plural = "Заказы"
    icon = "fa-solid fa-t-rex"


class OrderProductAdmin(ModelView, model=OrderProductModel):
    column_list = [
        OrderProductModel.order,
        OrderProductModel.product,
    ]
    can_delete = False
    name = "Заказ и продукты"
    name_plural = "Заказы и продукты"
    icon = "fa-solid fa-user"
