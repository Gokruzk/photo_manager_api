from fastapi import APIRouter, Path, File, UploadFile, status, Response, Form, HTTPException
from routes.image import ImageRoutes
from model.models  import ResponseSchema
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

        if data == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user has no images"
            )
        elif data == 3:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user does not exist"
            )
        elif data is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="An unexpected error occurred").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")


@router.post(path="", response_model_exclude_none=True)
async def upload_image(username: str = Form(...), file: UploadFile = File(...)):
    try:
        # get file type
        file_type = file.content_type.split('/')[-1]
        # rename image
        new_filename = f"{uuid.uuid4()}.{file_type}"
        file.filename = new_filename

        # send data
        data = await ImageRoutes.create(username, file)

        if data is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error uploading image"
            )
        elif data == 3:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user does not exist"
            )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Error uploading image").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully uploaded", result=file.filename).model_dump_json(), status_code=status.HTTP_201_CREATED, media_type="application/json")


@router.delete(path="/{cod_image}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_image(cod_image: int = Path(..., alias="cod_image")):
    try:
        
        img = await ImageRoutes.delete(cod_image)

        # if image exist delete
        if img == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The image does not exist"
            )
        elif img is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(
            ResponseSchema(
                detail="An unexpected error occurred").model_dump_json(),
            status_code=status.HTTP_400_BAD_REQUEST,
            media_type="application/json"
        )
    else:
        return Response(
            status_code=status.HTTP_204_NO_CONTENT,
            media_type="application/json"
        )
