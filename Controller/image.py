from fastapi import APIRouter, Path, File, UploadFile, status, Response
from Routes.image import ImageRoutes
from Model.models import UserImagesD
from schema import ResponseSchema
from pathlib import Path as pt
import uuid
import os

router = APIRouter(
    prefix="/images",
    tags=["Images"]
)

# folder to store images
home = pt.home()
images_folder = pt(home, "Images_Photo_Manager")
if not images_folder.exists():
    os.mkdir(images_folder)


@router.get(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all(username: str = Path(..., alias="username")):
    try:
        data = await ImageRoutes.get_all(username)
        if data is not False:
            return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")
        else:
            raise Exception("Error retreiving images")
    except Exception as e:
        return Response(ResponseSchema(detail=str(e)).model_dump_json(), status_code=status.HTTP_404_NOT_FOUND, media_type="application/json")


@router.post(path="", response_model_exclude_none=True)
async def upload_image(username: str, file: UploadFile = File(...)):
    # rename image
    file.filename = f"{uuid.uuid4()}.jpg"
    # send data
    await ImageRoutes.create(username, file)
    return Response(ResponseSchema(detail="Successfully uploaded", result=file.filename).model_dump_json(), status_code=status.HTTP_201_CREATED, media_type="application/json")


@router.delete(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_image(data: UserImagesD):
    try:
        img = await ImageRoutes.get_by_code(data.cod_image)
        if img is not False:
            await ImageRoutes.delete(data.cod_image, data.cod_user)
        else:
            raise Exception("Image does not exist")
    except Exception as e:
        print(e)
        return Response(
            ResponseSchema(
                detail=str(e)).model_dump_json(),
            status_code=status.HTTP_404_NOT_FOUND,
            media_type="application/json"
        )
    else:
        return Response(
            ResponseSchema(
                detail="Successfully deleted").model_dump_json(),
            status_code=status.HTTP_204_NO_CONTENT,
            media_type="application/json"
        )
