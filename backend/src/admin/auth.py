from typing import Optional
from fastapi import Response
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from fastapi.security.utils import get_authorization_scheme_param

from src.users.dependencies import get_current_user
from src.users.service import AuthService


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        user = await AuthService.authenticate_user(email, password)

        if user:
            token = await AuthService.create_token(user.id)
            request.session.update({"access_token": f"{token.access_token}"}) 
        
        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("access_token")
        _, param = get_authorization_scheme_param(token)  
        
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        user = await get_current_user(param)
        
        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        
        return True

authentication_backend = AdminAuth(secret_key="...")
