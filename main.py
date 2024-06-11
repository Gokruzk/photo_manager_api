import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from Config.db import conn
from Controller import country, image, user, auth
from fastapi.middleware.cors import CORSMiddleware


def init_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Server started")
        await conn.connect()
        yield
        print("Shutdown server")
        await conn.disconnect()
    app = FastAPI(
        title="Gokruzk",
        description="FastAPI Prisma",
        version="0.0.1",
        lifespan=lifespan
    )
    origins = [
        "http://localhost:3000"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def home():
        return "Welcome Home!"

    app.include_router(user.router)
    app.include_router(image.router)
    app.include_router(country.router)
    app.include_router(auth.router)

    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8888, reload=True)
