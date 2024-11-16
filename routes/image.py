from prisma.errors import RecordNotFoundError
from fastapi import File, UploadFile
from model.models import User_Images
from routes.user import UserRoutes
from datetime import datetime
from config.db import conn
from pathlib import Path
import os

# directory for images
home = Path.home()
images_folder = Path(home, "Images_Photo_Manager")


class ImageRoutes:
    @staticmethod
    async def get_all(username: str) -> list[User_Images]:
        try:
            # get user data
            user_retrieve = await UserRoutes.get_by_nick(username)

            if user_retrieve != []:
                # get user's images
                images: list[User_Images] = await conn.prisma.images.find_many(where={
                    "cod_user": user_retrieve.cod_user
                }, include={
                    "ubication": True,
                    "uploaded": True
                }
                )
                for image in images:
                    # return the image's name (the directory was mounted)
                    image.image = Path(image.image).name
                    # clean null data from schema.prisma
                    del image.ubication.Images
                    del image.ubication.User
                    del image.uploaded.User_Dates
                    del image.uploaded.Images
                    del image.user
            else:
                return 3
            
        except RecordNotFoundError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return images

    @staticmethod
    async def get_by_id(cod_image) -> User_Images:
        try:
            image = await conn.prisma.images.find_first(
                where={"cod_image": cod_image})

        except RecordNotFoundError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return image

    @staticmethod
    async def create(username: str, file: UploadFile = File(...)):
        try:
            # get user data
            user_retrieve = await UserRoutes.get_by_nick(username)

            if user_retrieve != []:
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
                    "cod_ubi": user_retrieve.cod_ubi,
                    "cod_user": user_retrieve.cod_user,
                    "image": str(image_path),
                    "uploadedat": uploadedAt
                })
            else:
                return 3

        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def delete(cod_image: int):
        try:

            img_retrieved = await ImageRoutes.get_by_id(cod_image)

            if img_retrieved == []:
                return []
            elif img_retrieved is False:
                return False
            else:
                # remove image from directory
                os.remove(Path(images_folder, img_retrieved.image))

                # remove database records
                await conn.prisma.images.delete(where={"cod_image": cod_image})

        except Exception as e:
            print(e)
            return False
