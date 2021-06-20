from datetime import timedelta, datetime
from typing import Optional, Union
from jose import jwt

from config import config
from core.repository import Repository
from users.helpers.password import verify_password
from users.models.user import UserModel


async def authenticate_user(
        repository: Repository,
        email: str,
        password: str
) -> Union[UserModel, bool]:
    if not (user := await repository.get(email=email)):
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        config.AUTH_SECRET_KEY,
        algorithm=config.AUTH_ALGORITHM
    )
