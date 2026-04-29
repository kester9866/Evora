import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import ADMIN_USERNAME, ADMIN_PASSWORD, JWT_SECRET

_password_hash = None


def _get_password_hash():
    global _password_hash
    if _password_hash is None:
        _password_hash = bcrypt.hashpw(
            ADMIN_PASSWORD.encode()[:72], bcrypt.gensalt()
        )
    return _password_hash


def verify_password(plain_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode()[:72], _get_password_hash())


def create_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except JWTError:
        return None
