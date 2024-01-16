from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from src.admin.views import (CartAdmin, 
                             UserAdmin, 
                             CartProductAdmin, 
                             ProductAdmin, 
                             CategoryAdmin, 
                             OrderAdmin, 
                             OrderProductAdmin)
from src.admin.auth import authentication_backend
from src.users.router import auth_router, user_router
from src.products.router import product_router
from src.carts.router import cart_router
from src.orders.router import order_router, promocode_router
from src.config import settings
from src.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(promocode_router)


admin = Admin(
    app, 
    engine,
    authentication_backend=authentication_backend
    )

admin.add_view(UserAdmin)
admin.add_view(CartAdmin)
admin.add_view(CartProductAdmin)
admin.add_view(ProductAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(OrderAdmin)
admin.add_view(OrderProductAdmin)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <a href="http://127.0.0.1:8000/docs">Documentation</a><br>
    <a href="http://127.0.0.1:8000/redoc">ReDoc</a>
    """
