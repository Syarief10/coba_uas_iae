from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError

from app.auth import verify_token


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = None

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            try:
                payload = verify_token(token)
                request.state.user = payload
            except JWTError:
                # Token invalid / expired → user tetap None
                pass

        response = await call_next(request)
        return response
