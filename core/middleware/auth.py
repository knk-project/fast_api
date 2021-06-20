import base64
import binascii

from jose import jwt, JWTError
from pydantic import EmailStr
from starlette.authentication import AuthenticationBackend, AuthenticationError, \
    AuthCredentials

from config import config
from core.exceptions.unauthorized import Unauthorized
from users.helpers.auth import authenticate_user
from users.repository import get_user_repo


class AuthMiddleware(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        scheme, token = auth.split()
        if scheme.lower() != 'bearer':
            return

        try:
            payload = jwt.decode(token, config.AUTH_SECRET_KEY, algorithms=[config.AUTH_ALGORITHM])
            email: EmailStr = payload.get("sub")
            if email is None:
                raise Unauthorized()
        except JWTError:
            raise Unauthorized()

        repository = await get_user_repo()
        user = await repository.get_or_404(email=email)
        if user is None:
            raise Unauthorized()

        return AuthCredentials(["authenticated"]), user
