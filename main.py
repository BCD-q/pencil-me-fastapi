from fastapi import FastAPI
from containers import Container
from fastapi.middleware.cors import CORSMiddleware

from routers import language_router, inspiration_router


def create_app() -> FastAPI:
    container = Container()
    app = FastAPI()
    app.container = container
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(language_router.router)
    app.include_router(inspiration_router.router)

    return app


app = create_app()
