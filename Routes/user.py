from Model.models import User
from Config.db import conn


class UserRoutes:

    @staticmethod
    async def get_all():
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
    async def get_by_coduser(cod_user: int):
        return await conn.prisma.user.find_first_or_raise(where={"cod_user": cod_user})

    @staticmethod
    async def delete(cod_user: int):
        return await conn.prisma.user.delete(where={"cod_user": cod_user})

    @staticmethod
    async def update(user: User, cod_user: int):
        return await conn.prisma.user.update(data={
            "cod_ubi": user.cod_ubi,
            "cod_state": user.cod_state,
            "username": user.username,
            "email": user.email,
            "password": user.password
        }, where={"cod_user": cod_user})
