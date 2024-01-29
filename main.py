from fastapi import FastAPI

from routers import LanguageRouter

app = FastAPI()

app.include_router(language.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
