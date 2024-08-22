from fastapi import APIRouter, Path, Depends, status, Response
from Utils.auth import JWTBearer, encryptPassword, signJWT
from Model.models import User, User
from Routes.user import UserRoutes
from schema import ResponseSchema
from Model.models import SignOut

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all():
    try:
        data = await UserRoutes.get_all()
    except Exception as e:
        print(e)
        return Response(content=ResponseSchema(detail="Error retreiving data", result=data).model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")


@router.get(path="/me")
async def read_user_me(token=Depends(JWTBearer())):
    try:
        user = await UserRoutes.read_user_me(token)
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Token error", result=user).model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST,media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=user).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")


@router.post(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_user(data: User):
    try:
        data.password = encryptPassword(data.password)
        user_retrieved = await UserRoutes.get_by_nick(data.username)
        if user_retrieved is False:
            await UserRoutes.create(data)
            user_retrieved = await UserRoutes.get_by_nick(data.username)
            user_retrieved = dict(user_retrieved)
            token = signJWT(user_retrieved['username'])
            sign_out = SignOut(token=token, user=user_retrieved)
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
        us = await UserRoutes.get_by_nick(username)
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
        user_retrieved = await UserRoutes.get_by_nick(user.username)
        if user_retrieved is False:
            user.password = encryptPassword(user.password)
            await UserRoutes.update(user, username)
        elif user_retrieved.cod_user == user.cod_user:
            user.password = encryptPassword(user.password)
            await UserRoutes.update(user, username)
        else:
            raise Exception
    except Exception as e:
        return Response(ResponseSchema(detail=f"The username already exist, {str(e)}").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT, media_type="application/json")
