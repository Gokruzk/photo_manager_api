import os
from pathlib import Path as pt
from fastapi import APIRouter, Path, File, UploadFile
from schema import ResponseSchema
from Routes.image import ImageRoutes
from Model.models import UserImagesD
import uuid

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)

# folder to store images
home = pt.home()
images_folder = pt(home, "Images_Photo_Manager")
if not images_folder.exists():
    os.mkdir(images_folder)
os.chdir(images_folder)


@router.get(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all(username: str = Path(..., alias="username")):
    data = await ImageRoutes.get_all(username)
    return ResponseSchema(status_code=200, detail="Successfully retreived", result=data)


@router.post(path="", response_model_exclude_none=True)
async def upload_image(username: str, file: UploadFile = File(...)):
    # rename image
    file.filename = f"{uuid.uuid4()}.jpg"
    # send data
    await ImageRoutes.create(username, file)
    return {"filename": file.filename}


@router.delete(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_image(data: UserImagesD):
    try:
        await ImageRoutes.delete(data.cod_image, data.cod_user)
        return ResponseSchema(status_code=200, detail="Successfully deleted")
    except Exception as e:
        return ResponseSchema(status_code=400, detail=e)
