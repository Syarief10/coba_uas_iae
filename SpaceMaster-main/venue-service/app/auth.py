from jose import jwt, JWTError

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"


class AuthError(Exception):
    pass


def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise AuthError("Invalid token")


def require_admin_from_context(info):
    request = info.context["request"]
    auth = request.headers.get("Authorization")

    if not auth:
        raise AuthError("Authorization header missing")

    token = auth.replace("Bearer ", "")
    payload = verify_token(token)

    if payload.get("role") != "admin":
        raise AuthError("Admin role required")

    return payload
