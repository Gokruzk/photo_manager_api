from Model.models import User, User_, Images, Dates, User_Dates, User_Images
from Config.db import conn
from fastapi import Depends
from datetime import datetime
from pathlib import Path
from Utils.auth import decodeJWT, JWTBearer

# images path
home = Path.home()
images_folder = Path(home, "DB_IMAGES")


class UserRoutes:

    @staticmethod
    async def get_all() -> list[User]:
        return await conn.prisma.user.find_many()

    @staticmethod
    async def create(data: User_):

        # folder to store images
        # if not images_folder.exists():
        #     os.mkdir(images_folder)
        # os.chdir(images_folder)

        user_post = await conn.prisma.user.create({
            "cod_ubi": data.cod_ubi,
            "cod_state": data.cod_state,
            "username": data.username,
            "email": data.email,
            "password": data.password
        })

        us = await conn.prisma.user.find_first_or_raise(
            where={"username": data.username})

        # data.image must be encoded in base64 in frontend then
        # decode and rename image to store in directory
        # if data.image != None:
        # user profile picture
        # image_post = await conn.prisma.images.create({
        #     "cod_ubi": data.cod_ubi,
        #     "image": base64_string
        # })
        # img = await conn.prisma.images.find_first_or_raise(where={"image": base64_string})
        # print(img.cod_image)
        # user_image = await conn.prisma.user_images.create({
        #     "cod_image": img.cod_image,
        #     "cod_user": us.cod_user,
        #     "description": data.image_description
        # })

        formatted_date = data.birth_date.strftime('%Y%m%d')
        birthday = int(formatted_date)
        formatted_date = datetime.now().strftime('%Y%m%d')
        created_date = int(formatted_date)

        user_dates = [await conn.prisma.user_dates.create({
            "cod_date": birthday,
            "cod_user": us.cod_user,
            "cod_description": 3
        }), await conn.prisma.user_dates.create({
            "cod_date": created_date,
            "cod_user": us.cod_user,
            "cod_description": 1
        }), await conn.prisma.user_dates.create({
            "cod_date": created_date,
            "cod_user": us.cod_user,
            "cod_description": 2
        })]
        return user_post, user_dates

    @staticmethod
    async def get_by_nick(username: str) -> User:
        return await conn.prisma.user.find_first_or_raise(where={"username": username})

    @staticmethod
    async def delete(username: str):
        us = await conn.prisma.user.find_first_or_raise(
            where={"username": username})
        await conn.prisma.user_dates.delete_many(where={"cod_user": us.cod_user})
        await conn.prisma.user.delete(where={"username": username})

    @staticmethod
    async def update(user: User, username: str):

        us = await conn.prisma.user.find_first_or_raise(
            where={"username": username})

        formatted_date = datetime.now().strftime('%Y%m%d')
        updated_date = int(formatted_date)

        await conn.prisma.user.update(data={
            "cod_ubi": user.cod_ubi,
            "cod_state": user.cod_state,
            "username": user.username,
            "email": user.email,
            "password": user.password
        }, where={"cod_user": us.cod_user})

        await conn.prisma.user_dates.update_many(data={
            "cod_date": updated_date,
            "cod_user": us.cod_user,
            "cod_description": 2
        }, where={"cod_user": us.cod_user, "cod_description": 2})

    @staticmethod
    async def read_user_me(token):
        decoded = decodeJWT(token)
        if "cod_user" in decoded:
            cod_user = decoded["cod_user"]
            return await conn.prisma.user.find_unique(where={"cod_user": cod_user})
        return None
