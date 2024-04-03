from fastapi import FastAPI
from containers import Container

from routers import language_router, inspiration_router


def create_app() -> FastAPI:
    container = Container()
    app = FastAPI()
    app.container = container
    app.include_router(language_router.router)
    app.include_router(inspiration_router.router)
    return app


app = create_app()
