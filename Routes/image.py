from fastapi import File, UploadFile
from Model.models import User_Images
from datetime import datetime
from Config.db import conn
from pathlib import Path

# directory for images
home = Path.home()
images_folder = Path(home, "Images_Photo_Manager")


class ImageRoutes:

    @staticmethod
    async def create(username: str, file: UploadFile = File(...)):
        us = await conn.prisma.user.find_first_or_raise(
            where={"username": username})

        # store image in directory
        contents = await file.read()
        image_path: str = Path(images_folder, file.filename)
        with open(f"{image_path}", "wb") as f:
            f.write(contents)

        # get current date
        formatted_date = datetime.now().strftime('%Y%m%d')
        uploadedAt = int(formatted_date)

        # store image in db
        await conn.prisma.images.create({
            "cod_ubi": us.cod_ubi,
            "image": str(image_path),
            "uploadedat": uploadedAt
        })

        # get image for the next step
        img = await conn.prisma.images.find_first_or_raise(
            where={"image": str(image_path)})

        # create field user_image in db
        await conn.prisma.user_images.create({
            "cod_image": img.cod_image,
            "cod_user": us.cod_user,
            "description": "New image"
        })

    @staticmethod
    async def get_all(username: str) -> list[User_Images]:
        us = await conn.prisma.user.find_first_or_raise(where={"username": username})
        return await conn.prisma.user_images.find_many(where={
            "cod_user": us.cod_user
        }, include={
            "images": {
                "include": {
                    "ubication": True,
                    "uploaded": True}
            }
        })

    @staticmethod
    async def delete(cod_image: int, cod_user: int):
        try:
            await conn.prisma.user_images.delete(where={"cod_image_cod_user": {"cod_image": cod_image, "cod_user": cod_user}})
            await conn.prisma.images.delete(where={"cod_image": cod_image})
        except Exception as e:
            print(e)
        # if (userimage_delete):
