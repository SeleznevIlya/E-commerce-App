from src.repository import BaseRepository
from src.users.models import UserModel, RefreshSessionModel
from src.users.schemas import UserCreateDB, UserUpdateDB, RefreshSessionCreate, RefreshSessionUpdate

class UserRepository(BaseRepository[UserModel, UserCreateDB, UserUpdateDB]):
    model = UserModel


class RefreshSessionRepository(BaseRepository[RefreshSessionModel, RefreshSessionCreate, RefreshSessionUpdate]):
    model = RefreshSessionModel
