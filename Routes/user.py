from Model.models import User, User_
from Config.db import conn
from datetime import datetime
from pathlib import Path
from Utils.auth import decodeJWT, JWTBearer

# images path
home = Path.home()
images_folder = Path(home, "DB_IMAGES")


class UserRoutes:

    @staticmethod
    async def get_all() -> list[User]:
        try:
            return await conn.prisma.user.find_many(
                include={
                    "User_Dates": {
                        "include": {"description": True}
                    },
                    "ubication": True
                }
            )
        except:
            return False

    @staticmethod
    async def create(data: User_):
        try:
            user_post = await conn.prisma.user.create({
                "cod_ubi": data.cod_ubi,
                "cod_state": data.cod_state,
                "username": data.username,
                "email": data.email,
                "password": data.password
            })

            us = await conn.prisma.user.find_first_or_raise(
                where={"username": data.username})

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
        except:
            return False

    @staticmethod
    async def get_by_nick(username: str) -> User:
        try:
            return await conn.prisma.user.find_first_or_raise(include={
                "User_Dates": {
                    "include": {"description": True}
                },
                "ubication": True
            }, where={"username": username})
        except:
            return False

    @staticmethod
    async def delete(username: str):
        try:
            us = await conn.prisma.user.find_first_or_raise(
                where={"username": username})
            await conn.prisma.user_dates.delete_many(where={"cod_user": us.cod_user})
            await conn.prisma.user_images.delete_many(where={"cod_user": us.cod_user})
            await conn.prisma.user.delete(where={"username": username})
        except:
            return False

    @staticmethod
    async def update(user: User, username: str):
        try:
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
            }, where={"cod_user": us.cod_user, "cod_description": 2})

            formatted_date = user.birth_date.strftime('%Y%m%d')
            birthday = int(formatted_date)

            await conn.prisma.user_dates.update_many(data={
                "cod_date": birthday
            }, where={"cod_user": us.cod_user, "cod_description": 3})
        except:
            return False

    @staticmethod
    async def read_user_me(token):
        decoded = decodeJWT(token)
        if "cod_user" in decoded:
            cod_user = decoded["cod_user"]
            return await conn.prisma.user.find_unique(where={"cod_user": cod_user})
        return None
