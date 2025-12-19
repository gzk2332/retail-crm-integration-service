from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.routes import routers
from core.settings import get_settings

settings = get_settings()


def register_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router, prefix=f'{settings.API_PREFIX}')


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    register_routers(app)
    yield


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
    )
