import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.carts.models import CartProductModel
from src.carts.repository import CartRepository


@pytest.mark.parametrize("email, fio, password, status_code",[
    ("qwerty@mail.ru", "qwerty", "qwerty", 201),
    ("qwerty@mail.ru", "qwerty", "qw123erty", 409),
    ("123qew", "qwerty", "qwerty", 422),
])
async def test_register(email, fio, password, status_code, ac: AsyncClient, session: AsyncSession):
    response = await ac.post("/api/v1/auth/register/", json=
                             {"email": email,
                              "fio": fio,
                              "password": password},
    )
    response_data = response.json()

    assert response.status_code == status_code
    
    if response.status_code == 201:
        users_cart = await CartRepository.find_one_with_association_model(
            session,
            CartProductModel.product,
            user_id=response_data["id"]
        )
        assert users_cart

@pytest.mark.parametrize("username, password, status_code",[
    ("test@test.com", "test", 200),
    # ("qwerty@mail.ru", "qwerty", 200),
    # ("qwerty@mail.ru", "uncorrect_password", 401),
])
async def test_login(username, password, status_code, ac: AsyncClient):
    response = await ac.post("/api/v1/auth/login", 
                            data={
                                "username": username,
                                "password": password
                                  },
                            headers={"content-type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == status_code
    if response.status_code == 200:
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"


async def test_verify_user(ac: AsyncClient):
    await ac.post("/api/v1/auth/login", 
                            data={
                                "username": "test@test.com",
                                "password": "test"
                                  },
                            headers={"content-type": "application/x-www-form-urlencoded"}
    )
    response = await ac.put("/user/verify")
    
    assert response.json()["message"] == "User was verified"
    assert response.json()["user"]['is_verified'] == True


async def test_logout(ac: AsyncClient):
    log = await ac.post("/api/v1/auth/login", 
                            data={
                                "username": "test@test.com",
                                "password": "test"
                                },
                            headers={"content-type": "application/x-www-form-urlencoded"}
    )
   
    response = await ac.post("/api/v1/auth/logout")
    # assert response.status_code == 200

    assert response.json() == {'message': 'Logged out successfully'}


