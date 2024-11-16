from datetime import datetime, timedelta, timezone
from typing import Dict
from os import getenv
import bcrypt
import jwt

secret = getenv("SECRET_KEY")


def encryptPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def validatePassword(password: str, encrypted: str) -> str:
    return bcrypt.checkpw(password.encode("utf-8"), encrypted.encode("utf-8"))


def signJWT(username: str) -> Dict[str, str]:
    EXPIRES = datetime.now(tz=timezone.utc) + timedelta(days=30)

    payload = {
        "exp": EXPIRES,
        "username": username,
    }
    token = jwt.encode(payload, secret, "HS256")
    return token
