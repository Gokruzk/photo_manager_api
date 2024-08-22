from fastapi import APIRouter, Path, Depends, status, Response
from Utils.auth import JWTBearer, encryptPassword, signJWT
from Model.models import User, User, SignToken
from Routes.user import UserRoutes
from schema import ResponseSchema

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all():
    try:
        # get all users
        data = await UserRoutes.get_all()
    except Exception as e:
        print(e)
        return Response(content=ResponseSchema(detail="Error retreiving data", result=data).model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")


@router.post(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_user(data: User):
    try:
        # encrypt password
        data.password = encryptPassword(data.password)
        # check if user does not exist
        user_retrieved = await UserRoutes.get_by_nick(data.username)
        if user_retrieved is False:
            # create user
            await UserRoutes.create(data)
            user_retrieved = await UserRoutes.get_by_nick(data.username)
            user_retrieved = dict(user_retrieved)
            # generate token
            token = signJWT(user_retrieved['username'])
            sign_out = SignToken(token=token, user=user_retrieved)
        else:
            raise Exception("The user already existe")
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail=str(e)).model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully created", result=sign_out).model_dump_json(), status_code=status.HTTP_201_CREATED, media_type="application/json")


@router.get(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_by_nick(username: str = Path(..., alias="username")):
    try:
        # get user by username
        data = await UserRoutes.get_by_nick(username)
        if not data:
            raise Exception
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail=str(e)).model_dump_json(), status_code=status.HTTP_404_NOT_FOUND, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")


@router.delete(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_user(username: str = Path(..., alias="username")):
    try:
        # get user by username
        us = await UserRoutes.get_by_nick(username)
        # delete if exist
        if us:
            await UserRoutes.delete(username)
        else:
            raise Exception("The user does not exist")
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail=str(e)).model_dump_json(), status_code=status.HTTP_404_NOT_FOUND, media_type="application/json")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT, media_type="application/json")


@router.put(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_user(user: User, username: str = Path(..., alias="username")):
    try:
        # get user by username to check if the username exist
        user_retrieved = await UserRoutes.get_by_nick(user.username)
        # if username does not exist
        if user_retrieved is False:
            # encrypt password
            user.password = encryptPassword(user.password)
            # update user
            await UserRoutes.update(user, username)
            print("Hola")
        # if username exist, check the cod_user
        elif user_retrieved.cod_user == user.cod_user:
            # encrypt password
            user.password = encryptPassword(user.password)
            # update user
            await UserRoutes.update(user, username)
        else:
            raise Exception
    except Exception as e:
        return Response(ResponseSchema(detail=f"The username already exist, {str(e)}").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT, media_type="application/json")
