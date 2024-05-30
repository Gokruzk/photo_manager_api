import os
from Model.models import Images
from Config.db import conn
from pathlib import Path
import base64

# folder to store images
# if not images_folder.exists():
#     os.mkdir(images_folder)
# os.chdir(images_folder)


class ImageRoutes:

    @staticmethod
    async def create(data: Images, username: str):
        us = await conn.prisma.user.find_first_or_raise(
            where={"username": username})

        # data.image must be encoded in base64 in frontend then
        # decode and rename image to store in directory
        image_path = ""

        await conn.prisma.images.create({
            "cod_ubi": data.cod_ubi,
            "image": image_path
        })

        img = await conn.prisma.images.find_first_or_raise(
            where={"image": image_path})
        
        await conn.prisma.user_images.create({
            "cod_image": img.cod_image,
            "cod_user": us.cod_user
        })

    @staticmethod
    async def get_all(username: str) -> Images:
        us = await conn.prisma.user.find_first_or_raise(
            where={"username": username})
        await conn.prisma.user_images.find_first_or_raise(where={"cod_user": us.cod_user})

    @staticmethod
    async def delete(username: str):
        return await conn.prisma.user.delete(where={"username": username})
