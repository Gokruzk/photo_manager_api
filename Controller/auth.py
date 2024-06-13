from fastapi import APIRouter
from Routes.user import UserRoutes
from Model.models import SignOut, SignIn
from Utils.auth import signJWT, validatePassword

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)


@router.post(path='/signin')
async def auth_user(user: SignIn):
    user_retrieved = await UserRoutes.get_by_nick(user.username)
    validated = validatePassword(user.password, user_retrieved.password)
    del user_retrieved.password
    del user_retrieved.state
    del user_retrieved.ubication
    del user_retrieved.User_Dates
    del user_retrieved.cod_ubi
    del user_retrieved.cod_state

    user_retrieved = dict(user_retrieved)
    if validated:
        token = signJWT(user_retrieved['cod_user'])
        sign_out = SignOut(token=token, user=user_retrieved)
        return sign_out
    return None
