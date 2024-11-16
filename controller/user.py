from fastapi import APIRouter, Path, status, Response, HTTPException
from model.models import User, User, SignToken, ResponseSchema
from routes.user import UserRoutes
from utils.auth import signJWT
from requests import post
from os import getenv

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_all():
    try:
        # get all users
        data = await UserRoutes.get_all()

        if data is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error retreiving data"
            )
        elif data == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No users registered"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Error retreiving data").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")


@router.get(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def get_by_nick(username: str = Path(..., alias="username")):
    try:
        # get user by username
        data = await UserRoutes.get_by_nick(username)

        if data is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error retreiving data"
            )
        elif data == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No user registered"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="Error retreiving data").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully retreived", result=data).model_dump_json(), status_code=status.HTTP_200_OK, media_type="application/json")


@router.post(path="", response_model=ResponseSchema, response_model_exclude_none=True)
async def create_user(data: User):
    try:
        user_created = await UserRoutes.create(data)

        API_EMAIL = getenv("API_EMAIL")

        # generate token
        token = signJWT(user_created.username)
        sign_out = SignToken(token=token, user=dict(user_created))

        if user_created is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif user_created == 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The user already exist"
            )
        else:
            email_data = {'email': user_created.email, 'message': f'{
                user_created.username}, le damos la bienvenida al sistema de gestión de imágenes'}
            # call email service
            email_response = post(f'{API_EMAIL}/email', json=email_data)

            if email_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="The user was created but the email was unable to sent"
                )

    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="An unexpected error occurred").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully created, check your email", result=sign_out).model_dump_json(), status_code=status.HTTP_201_CREATED, media_type="application/json")


@router.put(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def update_user(user: User, username: str = Path(..., alias="username")):
    try:
        data = await UserRoutes.update(user, username)

        if data is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An unexpected error occurred"
            )
        elif data == 2:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The username already exist"
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        return Response(ResponseSchema(detail="An unexpected error occurred").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT, media_type="application/json")


@router.delete(path="/{username}", response_model=ResponseSchema, response_model_exclude_none=True)
async def delete_user(username: str = Path(..., alias="username")):
    try:
        data = await UserRoutes.delete(username)

        if data == []:
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
        return Response(status_code=status.HTTP_204_NO_CONTENT, media_type="application/json")
