import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from Config.db import conn
from Controller import user


def init_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Server started")
        await conn.connect()
        yield
        print("Shutdown server")
        await conn.disconnect()
    app = FastAPI(
        title="Nigell Marcel Jama Oyarvide",
        description="FastAPI Prisma",
        version="1.0.0",
        lifespan=lifespan
    )

    @app.get("/")
    def home():
        return "Welcome Home!"

    app.include_router(user.router)

    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8888, reload=True)
