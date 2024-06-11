from fastapi import APIRouter, Path, Depends
from schema import ResponseSchema
from Routes.user import UserRoutes
from Model.models import User, User_
from Utils.auth import JWTBearer, encryptPassword

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
    return ResponseSchema(detail="Successfully created")


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
