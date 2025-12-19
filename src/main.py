import uvicorn
from fastapi import FastAPI

from core.server import init_middlewares, lifespan
from core.settings import get_settings

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        lifespan=lifespan,
        docs_url='/api/docs',
        redoc_url='/api/redoc',
        swagger_ui_parameters={'operationsSorter': 'method'},
    )
    init_middlewares(app)
    return app


if __name__ == '__main__':
    uvicorn.run(
        app='main:create_app',
        host=settings.HOST,
        port=settings.PORT,
        factory=True,
        reload=settings.AUTO_RELOAD,
    )
