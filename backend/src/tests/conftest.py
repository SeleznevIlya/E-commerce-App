import asyncio
import json
import pytest

from httpx import AsyncClient
from sqlalchemy import insert

from src.orders.models import OrderModel
from src.carts.models import CartModel, CartProductModel
from src.products.models import ProductModel

from src.config import settings
from src.database import Base, async_session_maker, engine
from src.users.models import UserModel
from src.main import app as fastapi_app
from src.users.models import UserModel


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"src/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    products = open_mock_json("products")
    carts = open_mock_json("cart")
    cart_product = open_mock_json("cart_product")
    order = open_mock_json("order")

    async with async_session_maker() as session:
        for Model, values in [
             (UserModel, users),
             (ProductModel, products),
             (CartModel, carts),
             (CartProductModel, cart_product),
             (OrderModel, order),
        ]:
            stmt = insert(Model).values(values)
            await session.execute(stmt)
        await session.commit()

	
@pytest.fixture(scope="session")
def event_loop(request):
	"""Create an instance of the default event loop for each test case."""
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()
     

@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        # response = await ac.post("/auth/login", 
        #                     data={
        #                         "username": username,
        #                         "password": password
        #                           },
        #                     headers={"content-type": "application/x-www-form-urlencoded"}
        #                     )
        # token = response.json().get("access_toker")
        # ac.headers["Authorization"] = f"Bearer {token}"
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
