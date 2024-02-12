from fastapi import FastAPI
from containers import Container

from routers import language_router


def create_app() -> FastAPI:
    container = Container()
    app = FastAPI()
    app.container = container
    app.include_router(language_router.router)
    return app

app = create_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
