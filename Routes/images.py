from Model.models import Images
from Config.db import conn
import base64


class ImageRoutes:

    @staticmethod
    async def create(data: Images):
        return await conn.prisma.images.create({

        })

    @staticmethod
    async def get_all(username: str) -> Images:
        us = await conn.prisma.user.find_first_or_raise(
            where={"username": username})
        await conn.prisma.user_images.find_first_or_raise(where={"cod_user": us.cod_user})

    @staticmethod
    async def delete(username: str):
        return await conn.prisma.user.delete(where={"username": username})
