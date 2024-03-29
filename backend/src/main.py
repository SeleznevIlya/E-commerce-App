from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from prometheus_fastapi_instrumentator import Instrumentator

from src.admin.auth import authentication_backend
from src.admin.views import (
    CartAdmin,
    CartProductAdmin,
    CategoryAdmin,
    OrderAdmin,
    OrderProductAdmin,
    ProductAdmin,
    UserAdmin,
)
from src.carts.router import cart_router
from src.config import settings
from src.database import engine
from src.orders.router import order_router, promocode_router
from src.products.router import product_router
from src.users.router import auth_router, user_router
from src.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("service started")
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    logger.info("redis started")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    logger.info("service stopped")


app = FastAPI(
    lifespan=lifespan,
)


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)



app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(promocode_router)


admin = Admin(app, engine, authentication_backend=authentication_backend)

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
