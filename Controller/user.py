from fastapi import APIRouter, Path
from schema import ResponseSchema
from Routes.user import UserRoutes
from Model.models import User
from passlib.hash import sha256_crypt

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all():
    data = await UserRoutes.get_all()
    return ResponseSchema(detail="Successfully retreived", result=data)


@router.post(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_user(data: User):
    data.password = sha256_crypt.encrypt(data.password)
    await UserRoutes.create(data)
    return ResponseSchema(detail="Successfully created")


@router.get(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_by_nick(username: int = Path(..., alias="username")):
    data = await UserRoutes.get_by_coduser(username)
    return ResponseSchema(detail="Successfully retreived", result=data)


@router.delete(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_user(username: str = Path(..., alias="username")):
    await UserRoutes.delete(username)
    return ResponseSchema(detail="Successfully deleted")


@router.put(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_user(user: User, username: str = Path(..., alias="username")):
    await UserRoutes.update(user, username)
    return ResponseSchema(detail="Successfully updated")
