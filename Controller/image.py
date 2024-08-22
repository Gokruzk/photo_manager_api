from fastapi import APIRouter, Path, File, UploadFile, status, Response, Form
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
        # get all user's images
        data = await ImageRoutes.get_all(username)
        if data is not False:
            return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")
        else:
            raise Exception("Error retreiving images")
    except Exception as e:
        return Response(ResponseSchema(detail=str(e)).model_dump_json(), status_code=status.HTTP_404_NOT_FOUND, media_type="application/json")


@router.post(path="", response_model_exclude_none=True)
async def upload_image(username: str = Form(...), file: UploadFile = File(...)):
    try:
        # get file type
        file_type = file.content_type.split('/')[-1]
        # rename image
        new_filename = f"{uuid.uuid4()}.{file_type}"
        file.filename = new_filename
        # send data
        await ImageRoutes.create(username, file)
        return Response(ResponseSchema(detail="Successfully uploaded", result=file.filename).model_dump_json(), status_code=status.HTTP_201_CREATED, media_type="application/json")
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Error uploading image").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")


@router.delete(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_image(data: UserImagesD):
    try:
        # get image by 
        img = await ImageRoutes.get_by_id(data.cod_image)
        # if image exist
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
            status_code=status.HTTP_204_NO_CONTENT,
            media_type="application/json"
        )
