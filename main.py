from fastapi import FastAPI

from routers import Language

app = FastAPI()

app.include_router(Language.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
