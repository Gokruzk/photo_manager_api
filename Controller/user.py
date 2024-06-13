from fastapi import APIRouter, Path, Depends
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
    data = await UserRoutes.get_all()
    return ResponseSchema(detail="Successfully retreived", result=data)


@router.get(path="/me")
async def read_user_me(token=Depends(JWTBearer())):
    user = await UserRoutes.read_user_me(token)
    return ResponseSchema(detail="Successfully retreived", result=user)


@router.post(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_user(data: User_):
    data.password = encryptPassword(data.password)
    
    await UserRoutes.create(data)
    user_retrieved = await UserRoutes.get_by_nick(data.username)
    del user_retrieved.password
    del user_retrieved.state
    del user_retrieved.ubication
    del user_retrieved.User_Dates
    del user_retrieved.cod_ubi
    del user_retrieved.cod_state

    user_retrieved = dict(user_retrieved)
    token = signJWT(user_retrieved['cod_user'])
    sign_out = SignOut(token=token, user=user_retrieved)

    return ResponseSchema(detail="Successfully created", result=sign_out)


@router.get(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_by_nick(username: str = Path(..., alias="username")):
    data = await UserRoutes.get_by_nick(username)
    return ResponseSchema(detail="Successfully retreived", result=data)


@router.delete(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_user(username: str = Path(..., alias="username")):
    await UserRoutes.delete(username)
    return ResponseSchema(detail="Successfully deleted")


@router.put(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_user(user: User, username: str = Path(..., alias="username")):
    user.password = encryptPassword(user.password)
    await UserRoutes.update(user, username)
    return ResponseSchema(detail="Successfully updated")
