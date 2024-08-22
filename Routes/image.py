from fastapi import File, UploadFile
from Model.models import User_Images
from datetime import datetime
from Config.db import conn
from pathlib import Path
import os

# directory for images
home = Path.home()
images_folder = Path(home, "Images_Photo_Manager")


class ImageRoutes:

    @staticmethod
    async def create(username: str, file: UploadFile = File(...)):
        try:
            # get user data
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
        except Exception as e:
            return False

    @staticmethod
    async def get_all(username: str) -> list[User_Images]:
        try:
            # get user data
            us = await conn.prisma.user.find_first_or_raise(where={"username": username})

            # get user's images
            images: list[User_Images] = await conn.prisma.user_images.find_many(where={
                "cod_user": us.cod_user
            }, include={
                "images": {
                    "include": {
                        "ubication": True,
                        "uploaded": True}
                }
            })
            for image in images:
                # return the image's name (the directory was mounted)
                image.images.image = Path(image.images.image).name
                # clean null data from schema.prisma
                del image.images.ubication.Images
                del image.images.ubication.User
                del image.images.User_Images
                del image.images.uploaded.User_Dates
                del image.images.uploaded.Images
                del image.user
            return images
        except:
            return False

    @staticmethod
    async def get_by_id(cod_image: int) -> list[User_Images]:
        try:
            # get image
            return await conn.prisma.images.find_first_or_raise(where={"cod_image": cod_image})
        except:
            return False

    @staticmethod
    async def delete(cod_image: int, cod_user: int):
        try:
            # get image data
            img = await conn.prisma.images.find_first_or_raise(where={
                "cod_image": cod_image
            })
            # remove image from directory
            os.remove(img.image)

            # remove database records
            await conn.prisma.user_images.delete(where={"cod_image_cod_user": {"cod_image": cod_image, "cod_user": cod_user}})
            await conn.prisma.images.delete(where={"cod_image": cod_image})
        except:
            return False
