from Model.models import User
from Config.db import conn


class UserRoutes:

    @staticmethod
    async def get_all() -> list[User]:
        return await conn.prisma.user.find_many()

    @staticmethod
    async def create(user: User):
        return await conn.prisma.user.create({
            "cod_ubi": user.cod_ubi,
            "cod_state": user.cod_state,
            "username": user.username,
            "email": user.email,
            "password": user.password
        })

    @staticmethod
    async def get_by_nick(username: str) -> User:
        return await conn.prisma.user.find_first_or_raise(where={"username": username})

    @staticmethod
    async def delete(username: str):
        return await conn.prisma.user.delete(where={"username": username})

    @staticmethod
    async def update(user: User, username: str):
        return await conn.prisma.user.update(data={
            "cod_ubi": user.cod_ubi,
            "cod_state": user.cod_state,
            "username": user.username,
            "email": user.email,
            "password": user.password
        }, where={"username": username})
