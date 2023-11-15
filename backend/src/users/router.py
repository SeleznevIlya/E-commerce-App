import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, Response, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import UserCreate, User, Token, UserUpdate
from .service import UserService, AuthService
from ..exceptions import InvalidCredentialsException
from ..config import settings
from .models import UserModel
from .dependencies import get_current_active_user, get_current_user, get_current_superuser, get_current_verified_user


auth_router = APIRouter(prefix="/auth", tags=["auth"])
user_router = APIRouter(prefix="/user", tags=["user"])


@auth_router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate) -> User:
    return await UserService.create_new_user(user)


@auth_router.post("/login")
async def login(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends()
) -> Token:
    user = await AuthService.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise InvalidCredentialsException
    
    token = await AuthService.create_token(user.id)
    response.set_cookie(
        "access_token",
        token.access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60,
        httponly=True
    )
    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS*30*24*60,
        httponly=True
    )
    return token


@auth_router.post("/logout")
async def logout(request: Request,
                 response: Response,
                 user: UserModel = Depends(get_current_active_user)):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    await AuthService.logout(request.cookies.get("refresh_token"))
    return {"message": "Logged out successfully"}


@auth_router.post("/refresh")
async def refresh_token(
    response: Response,
    request: Request
) -> Token:
    new_token = await AuthService.refresh_token(
        uuid.UUID(request.cookies.get("refresh_token"))
    )

    response.set_cookie(
        "access_token",
        new_token.access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60,
        httponly=True
    )
    response.set_cookie(
        "refresh_token",
        new_token.refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS*30*24*60,
        httponly=True
    )
    return new_token


@auth_router.post("/abort")
async def abort_all_sessions(
    response: Response,
    user: UserModel = Depends(get_current_user)
):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    
    await AuthService.abort_all_session(user_id=user.id)
    return {"message": "All session was aborted"}


@user_router.get("")
async def get_user_list(
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
        current_user: UserModel = Depends(get_current_superuser)
) -> List[User]:
    return await UserService.get_user_list(offset=offset, limit=limit)


@user_router.delete("/me")
async def delete_current_user(
    response: Response,
    request: Request,
    current_user: UserModel = Depends(get_current_user)
):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    await AuthService.logout(request.cookies.get("refresh_token"))
    await UserService.delete_user(current_user.id)
    return {"message": "User status is not active already"}


@user_router.get("/me")
async def get_current_user_me(
    current_user: UserModel = Depends(get_current_active_user)
) -> User:
    return await UserService.get_user(user_id=current_user.id)


@user_router.put("/me")
async def update_current_user(
    user: UserUpdate,
    current_user: UserModel = Depends(get_current_user)
) -> User:
    return await UserService.update_user(current_user.id, user)


@user_router.put("/verify")
async def verify_current_user(
    # user: UserUpdate,
    current_user: UserModel = Depends(get_current_user)
):
    verified_user = await UserService.verify_user(current_user.id)
    return {"message": "User was verified",
            "user": verified_user}


@user_router.get("/{user_id}")
async def get_user(
    user_id: str,
    current_user: UserModel = Depends(get_current_superuser)
) -> User:
    return await UserService.get_user(user_id=user_id)


@user_router.put("/{user_id}")
async def update_user(
    user_id: str,
    user: User,
    current_user: UserModel = Depends(get_current_superuser)
) -> User:
    return await UserService.update_user_from_superuser(user_id, user)


@user_router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: UserModel = Depends(get_current_superuser)
):
    await UserService.delete_user_from_superuser(user_id)
    return {"message": "User was deleted"}


