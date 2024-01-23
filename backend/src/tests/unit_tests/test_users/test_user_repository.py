import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.repository import UserRepository


@pytest.mark.parametrize('email, exists', [
	("test@test.com", True),
	("ilya@example.com", True),
	("ilya123@example.com", False)
    ]
)
async def test_find_user_by_email(email, exists, session: AsyncSession):
	user = await UserRepository.find_one_or_none(session, email=email)
	if exists:
		assert user
		assert user.email == email
	else:
		assert not user
		

@pytest.mark.parametrize('email, exists', [
	("test@test.com", True),
	("ilya@example.com", True),
	("ilya123@example.com", False)
    ]
)
async def test_delete_user_by_email(email, exists, session: AsyncSession):
	user = await UserRepository.find_one_or_none(session, email=email)
	
	if exists:
		assert user
		await UserRepository.delete(session, email=email)
		user_1 = await UserRepository.find_one_or_none(session, email=email)
		assert not user_1
	else:
		assert not user
