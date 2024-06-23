from fastapi import APIRouter, status, HTTPException
from Routes.user import UserRoutes
from Model.models import SignOut, SignIn
from Utils.auth import signJWT, validatePassword
from schema import ResponseSchema

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)


@router.post(path='/signin')
async def auth_user(user: SignIn):
    try:
        user_retrieved = await UserRoutes.get_by_nick(user.username)
        if user_retrieved:
            validated = validatePassword(
                user.password, user_retrieved.password)
            if validated:
                del user_retrieved.password
                del user_retrieved.state
                del user_retrieved.ubication
                del user_retrieved.User_Dates
                del user_retrieved.cod_ubi
                del user_retrieved.cod_state

                user_retrieved = dict(user_retrieved)
                token = signJWT(user_retrieved['cod_user'])
                sign_out = SignOut(token=token, user=user_retrieved)
            else:
                raise Exception
        else:
            raise Exception
    except Exception as e:
        print(e)
        return ResponseSchema(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password incorrect")
    else:
        return ResponseSchema(status_code=status.HTTP_200_OK, detail="Successfully authenticated", result=sign_out)
