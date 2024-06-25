from fastapi import APIRouter, Path, Depends, status, HTTPException
from schema import ResponseSchema
from Routes.user import UserRoutes
from Model.models import User, User_
from Utils.auth import JWTBearer, encryptPassword, signJWT
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
        return ResponseSchema(status_code=status.HTTP_400_BAD_REQUEST, detail="Error retreiving data", result=data)
    else:
        return ResponseSchema(status_code=status.HTTP_200_OK, detail="Successfully retreived", result=data)


@router.get(path="/me")
async def read_user_me(token=Depends(JWTBearer())):
    try:
        user = await UserRoutes.read_user_me(token)
    except Exception as e:
        print(e)
        return ResponseSchema(status_code=status.HTTP_400_BAD_REQUEST, detail="Token error", result=user)
    else:
        return ResponseSchema(status_code=status.HTTP_200_OK, detail="Successfully retreived", result=user)


@router.post(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_user(data: User_):
    try:
        data.password = encryptPassword(data.password)
        user_retrieved = await UserRoutes.get_by_nick(data.username)
        if user_retrieved is False:
            await UserRoutes.create(data)
            user_retrieved = await UserRoutes.get_by_nick(data.username)
            del user_retrieved.password
            del user_retrieved.state
            del user_retrieved.ubication
            del user_retrieved.User_Dates
            del user_retrieved.cod_ubi
            del user_retrieved.cod_state
            del user_retrieved.cod_user

            user_retrieved = dict(user_retrieved)
            token = signJWT(user_retrieved['username'])
            sign_out = SignOut(token=token, user=user_retrieved)
        else:
            raise Exception
    except Exception as e:
        print(e)
        return ResponseSchema(status_code=status.HTTP_400_BAD_REQUEST, detail="The user already exist")
    else:
        return ResponseSchema(status_code=status.HTTP_201_CREATED, detail="Successfully created", result=sign_out)


@router.get(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_by_nick(username: str = Path(..., alias="username")):
    try:
        data = await UserRoutes.get_by_nick(username)
        if not data:
            raise Exception
    except Exception as e:
        print(e)
        return ResponseSchema(status_code=status.HTTP_204_NO_CONTENT, detail="The user does not exist")
    else:
        return ResponseSchema(status_code=status.HTTP_200_OK, detail="Successfully retreived", result=data)


@router.delete(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_user(username: str = Path(..., alias="username")):
    try:
        await UserRoutes.delete(username)
    except Exception as e:
        print(e)
        return ResponseSchema(status_code=status.HTTP_204_NO_CONTENT, detail="The user does not exist")
    else:
        return ResponseSchema(status_code=status.HTTP_200_OK, detail="Successfully deleted")


@router.put(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_user(user: User, username: str = Path(..., alias="username")):
    try:
        user.password = encryptPassword(user.password)
        await UserRoutes.update(user, username)
    except Exception as e:
        print(e)
        return ResponseSchema(status_code=status.HTTP_400_BAD_REQUEST, detail="Error updating user")
    else:
        return ResponseSchema(status_code=status.HTTP_200_OK, detail="Successfully updated")
