from src.repository import BaseRepository
from src.users.models import RefreshSessionModel, UserModel
from src.users.schemas import (
    RefreshSessionCreate,
    RefreshSessionUpdate,
    UserCreateDB,
    UserUpdateDB,
)


class UserRepository(BaseRepository[UserModel, UserCreateDB, UserUpdateDB]):
    model = UserModel


class RefreshSessionRepository(BaseRepository[RefreshSessionModel, RefreshSessionCreate, RefreshSessionUpdate]):
    model = RefreshSessionModel
