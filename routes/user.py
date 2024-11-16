from model.models import User, User, User_Retrieve
from prisma.errors import RecordNotFoundError
from utils.auth import encryptPassword
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
                del user.Images
                del user.ubication.Images
                del user.ubication.User
                del user.state
                for user_date in user.User_Dates:
                    del user_date.user
                    del user_date.date
                    del user_date.description.User_Dates

        except RecordNotFoundError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return users

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
            del user.ubication.Images
            del user.ubication.User
            del user.state
            for user_date in user.User_Dates:
                del user_date.user
                del user_date.date
                del user_date.description.User_Dates

        except RecordNotFoundError:
            return []
        except Exception as e:
            print(e)
            return False
        else:
            return user

    @staticmethod
    async def create(data: User):
        try:
            # check if user exist
            user_retrieved = await UserRoutes.get_by_nick(data.username)

            if user_retrieved != []:
                return 1
            else:
                # insert in user's table
                user_post = await conn.prisma.user.create({
                    "cod_ubi": data.cod_ubi,
                    "cod_state": data.cod_state,
                    "username": data.username,
                    "email": data.email,
                    "password": encryptPassword(data.password)
                })

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
                    "cod_user": user_post.cod_user,
                    "cod_description": 3
                })
                await conn.prisma.user_dates.create({
                    "cod_date": created_date,
                    "cod_user": user_post.cod_user,
                    "cod_description": 1
                })
                await conn.prisma.user_dates.create({
                    "cod_date": created_date,
                    "cod_user": user_post.cod_user,
                    "cod_description": 2
                })

        except Exception as e:
            print(e)
            return False
        else:
            return user_post

    @staticmethod
    async def update(user: User, username: str):
        try:
            # get user by username to check if the username exist
            user_retrieved = await UserRoutes.get_by_nick(username)
            # if username does not exist
            if user_retrieved is []:
                # encrypt password
                user.password = encryptPassword(user.password)
            # if username exist, check the cod_user
            elif user_retrieved.cod_user == user.cod_user:
            # encrypt password
                user.password = encryptPassword(user.password)
            else:
                return 2
            
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
            }, where={"cod_user": user_retrieved.cod_user})

            # update dates
            await conn.prisma.user_dates.update_many(data={
                "cod_date": updated_date,
            }, where={"cod_user": user_retrieved.cod_user, "cod_description": 2})

            formatted_date = user.birthdate.strftime('%Y%m%d')
            birthday = int(formatted_date)

            await conn.prisma.user_dates.update_many(data={
                "cod_date": birthday
            }, where={"cod_user": user_retrieved.cod_user, "cod_description": 3})
        
        except Exception as e:
            print(e)
            return False

    @staticmethod
    async def delete(username: str):
        try:
            from routes.image import ImageRoutes
            # get user by username
            user_retrieved = await UserRoutes.get_by_nick(username)
            # delete if exist
            if user_retrieved == []:
                return []
            else:
                # delete dates, images, user
                await conn.prisma.user_dates.delete_many(where={"cod_user": user_retrieved.cod_user})
                images = await ImageRoutes.get_all(user_retrieved.username)
                for image in images:
                    await ImageRoutes.delete(image.cod_image)
                await conn.prisma.user.delete(where={"username": user_retrieved.username})

        except Exception as e:
            print(e)
            return False
