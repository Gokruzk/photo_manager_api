from model.models import User, User, User_Retrieve
from routes.image import ImageRoutes
from datetime import datetime
from config.db import conn
from pathlib import Path

# images path
home = Path.home()
images_folder = Path(home, "DB_IMAGES")


class UserRoutes:
    @staticmethod
    async def get_all() -> list[User_Retrieve]:
        try:
            users = await conn.prisma.user.find_many(
                include={
                    "User_Dates": {
                        "include": {"description": True}
                    },
                    "ubication": True
                })

            # clean null data from schema.prisma
            for user in users:
                del user.User_Images
                del user.ubication.Images
                del user.ubication.User
                del user.state
                for user_date in user.User_Dates:
                    del user_date.user
                    del user_date.date
                    del user_date.description.User_Dates

            # return user
            return users
        except:
            return False

    @staticmethod
    async def get_by_nick(username: str) -> User_Retrieve:
        try:
            # retrieve user
            user: User_Retrieve = await conn.prisma.user.find_first_or_raise(include={
                "User_Dates": {
                    "include": {"description": True}
                },
                "ubication": True
            }, where={"username": username})

            # clean null data from schema.prisma
            del user.User_Images
            del user.ubication.Images
            del user.ubication.User
            del user.state
            for user_date in user.User_Dates:
                del user_date.user
                del user_date.date
                del user_date.description.User_Dates

            # return user
            return user
        except:
            return False

    @staticmethod
    async def create(data: User):
        try:
            # insert in user's table
            user_post = await conn.prisma.user.create({
                "cod_ubi": data.cod_ubi,
                "cod_state": data.cod_state,
                "username": data.username,
                "email": data.email,
                "password": data.password
            })

            # retrieve user created for get the autoincremental code
            user_retrieve = await conn.prisma.user.find_first_or_raise(
                where={"username": data.username})

            # format date to YYYYMMDD
            formatted_date = data.birthdate.strftime('%Y%m%d')
            # parse to int
            birthday = int(formatted_date)
            # get current date
            formatted_date = datetime.now().strftime('%Y%m%d')
            # parse to int
            created_date = int(formatted_date)

            await conn.prisma.user_dates.create({
                "cod_date": birthday,
                "cod_user": user_retrieve.cod_user,
                "cod_description": 3
            })
            await conn.prisma.user_dates.create({
                "cod_date": created_date,
                "cod_user": user_retrieve.cod_user,
                "cod_description": 1
            })
            await conn.prisma.user_dates.create({
                "cod_date": created_date,
                "cod_user": user_retrieve.cod_user,
                "cod_description": 2
            })
            return user_post
        except:
            return False

    @staticmethod
    async def update(user: User, username: str):
        try:
            # retrieve user
            user_retrieve = await conn.prisma.user.find_first_or_raise(
                where={"username": username})

            # format current date
            formatted_date = datetime.now().strftime('%Y%m%d')
            # parse to int
            updated_date = int(formatted_date)

            # update user data
            await conn.prisma.user.update(data={
                "cod_ubi": user.cod_ubi,
                "cod_state": user.cod_state,
                "username": user.username,
                "email": user.email,
                "password": user.password
            }, where={"cod_user": user_retrieve.cod_user})

            # update dates
            await conn.prisma.user_dates.update_many(data={
                "cod_date": updated_date,
            }, where={"cod_user": user_retrieve.cod_user, "cod_description": 2})

            formatted_date = user.birthdate.strftime('%Y%m%d')
            birthday = int(formatted_date)

            await conn.prisma.user_dates.update_many(data={
                "cod_date": birthday
            }, where={"cod_user": user_retrieve.cod_user, "cod_description": 3})
        except:
            return False

    @staticmethod
    async def delete(user_retrieve: User):
        try:
            # delete dates, images, user
            await conn.prisma.user_dates.delete_many(where={"cod_user": user_retrieve.cod_user})
            images = await ImageRoutes.get_all(user_retrieve.username)
            for image in images:
                await ImageRoutes.delete(image.cod_image)
            await conn.prisma.user.delete(where={"username": user_retrieve.username})

        except:
            return False
