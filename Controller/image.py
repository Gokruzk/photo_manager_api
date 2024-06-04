from fastapi import APIRouter, Path
from schema import ResponseSchema
from Routes.image import ImageRoutes
from Model.models import Images

router = APIRouter(
    prefix="/images",
    tags=["images"]
)


@router.get(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all(username: str = Path(..., alias="username")):
    data = await ImageRoutes.get_all(username)
    return ResponseSchema(detail="Successfully retreived", result=data)


@router.post(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_user(data: Images):
    await ImageRoutes.create(data)
    return ResponseSchema(detail="Successfully created")


@router.delete(path="/{id}/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_image(id: str = Path(..., alias="id"), username: str = Path(..., alias="username")):
    await ImageRoutes.delete(id, username)
    return ResponseSchema(detail="Successfully deleted")
