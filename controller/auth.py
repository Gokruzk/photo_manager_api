from utils.auth import signJWT, validatePassword
from model.models import SignToken, SignIn, ResponseSchema
from fastapi import APIRouter, status, Response, HTTPException
from routes.user import UserRoutes

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)


@router.post(path='/signin')
async def auth_user(user: SignIn):
    try:
        # check if user exist
        user_retrieved = await UserRoutes.get_by_nick(user.username)
        if user_retrieved != []:
            # valide password
            validated = validatePassword(
                user.password, user_retrieved.password)
            if validated:
                del user_retrieved.password
                user_retrieved = dict(user_retrieved)
                # generate token
                token = signJWT(user_retrieved['username'])
                sign_out = SignToken(token=token, user=user_retrieved)
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Username or password incorrect"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The user does not exist"
            )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        return Response(ResponseSchema(detail="An unexpected error occurred").model_dump_json(), status_code=status.HTTP_400_BAD_REQUEST, media_type="application/json")
    else:
        return Response(ResponseSchema(detail="Successfully authenticated", result=sign_out).model_dump_json(),status_code=status.HTTP_200_OK, media_type="application/json")
