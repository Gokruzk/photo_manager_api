from Utils.auth import signJWT, validatePassword
from Model.models import SignToken, SignIn
from fastapi import APIRouter, status
from Routes.user import UserRoutes
from schema import ResponseSchema

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)


@router.post(path='/signin')
async def auth_user(user: SignIn):
    try:
        # check if user exist
        user_retrieved = await UserRoutes.get_by_nick(user.username)
        if user_retrieved:
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
                raise Exception
        else:
            raise Exception
    except Exception as e:
        print(e)
        return ResponseSchema(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password incorrect")
    else:
        return ResponseSchema(status_code=status.HTTP_200_OK, detail="Successfully authenticated", result=sign_out)
