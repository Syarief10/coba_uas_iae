from jose import jwt, JWTError
from fastapi import HTTPException

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"


def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_admin(info):
    request = info.context["request"]
    auth = request.headers.get("Authorization")

    if not auth:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = auth.replace("Bearer ", "")
    payload = verify_token(token)

    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")

    return payload
