import asyncio
import json
from httpx import AsyncClient
import pytest
from sqlalchemy import insert
from src.config import settings
from src.database import Base, async_session_maker, engine
from src.users.models import UserModel
from src.main import app as fastapi_app
from src.users.models import UserModel
from src.users.utils import get_password_hash



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

    async with async_session_maker() as session:
        stmt = insert(UserModel).values(users)

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
          yield ac
