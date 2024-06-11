import jwt
import bcrypt
from os import getenv
from datetime import datetime, timedelta, timezone
from typing import Dict
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

jwtSecret = getenv("SECRET_KEY")


def encryptPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def validatePassword(password: str, encrypted: str) -> str:
    return bcrypt.checkpw(password.encode("utf-8"), encrypted.encode("utf-8"))

def signJWT(cod_user: str) -> Dict[str, str]:
    EXPIRES = datetime.now(tz=timezone.utc) + timedelta(days=365)

    payload = {
        "exp": EXPIRES,
        "cod_user": cod_user,
    }
    token = jwt.encode(payload, jwtSecret, getenv("ALGORITHM"))

    return token


def decodeJWT(token: str) -> dict:
    try:
        decoded = jwt.decode(token, jwtSecret, getenv("ALGORITHM"))
        return decoded if decoded["exp"] else None
    except jwt.ExpiredSignatureError:
        print("Token expired. Get new one")
        return None
    except:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtToken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtToken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
