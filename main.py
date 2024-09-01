from fastapi.middleware.cors import CORSMiddleware
from controller import country, image, user, auth
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.db import conn
from pathlib import Path
import uvicorn

home = Path.home()
images_folder = Path(home, "Images_Photo_Manager")

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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def home():
        return "Photo manager API!"

    app.include_router(user.router)
    app.include_router(image.router)
    app.include_router(country.router)
    app.include_router(auth.router)
    # mount directory
    app.mount("/images/image", StaticFiles(directory=images_folder), name="images")

    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8888, reload=True)
