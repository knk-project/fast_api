from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from config import config
from core.repository import Repository
from users.helpers.auth import authenticate_user, create_access_token
from users.models.token import Token
from users.models.user import UserModel
from users.repository import get_user_repo
from users.serializers.user import UserSerializer


def get_auth_router() -> APIRouter:
    router = APIRouter()

    @router.post('/register/', response_model=UserModel)
    async def create_user(
            user: UserModel,
            repository: Repository = Depends(get_user_repo)
    ):
        # Store
        user.last_login = datetime.now()
        user.is_active = True
        instance = await repository.create(user)

        # Serialize instance
        serializer = UserSerializer(instance)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=serializer.data)

    @router.post("/login/", response_model=Token)
    async def login_for_access_token(
            form_data: OAuth2PasswordRequestForm = Depends(),
            repository: Repository = Depends(get_user_repo)
    ):
        # Auth with credentials
        user: UserModel = await authenticate_user(
            repository, form_data.username, form_data.password
        )

        # Credentials not match
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Update last_login value
        await repository.update(user.id, dict(last_login=datetime.now()))

        # Create token
        access_token_expires = timedelta(minutes=config.AUTH_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    return router
