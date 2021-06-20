from typing import List

from fastapi import APIRouter, Depends, Body
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from core.models import PyObjectId
from core.permissions.auth import is_admin_or_owner
from core.repository import Repository
from users.models.user import UserModel
from users.repository import get_user_repo
from users.serializers.user import UserSerializer


def get_crud_router() -> APIRouter:
    router = APIRouter()

    @router.post('/', response_model=UserModel)
    @is_admin_or_owner
    async def create_user(
            request: Request,
            user: UserModel,
            repository: Repository = Depends(get_user_repo)
    ):
        # Store
        instance = await repository.create(user)

        # Serialize instance
        serializer = UserSerializer(instance)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=serializer.data)

    @router.get('/list/', response_model=List[UserModel])
    async def list_users(repository: Repository = Depends(get_user_repo)):
        instances = await repository.list(jsonable=True)

        # Serialize instance
        serializer = UserSerializer(instances, many=True)
        return JSONResponse(content=serializer.data)

    @router.get('/{instance_id}/', response_model=UserModel)
    async def show_user(
            instance_id: PyObjectId,
            repository: Repository = Depends(get_user_repo)
    ):
        # Retrieve user
        user = await repository.get_or_404(_id=instance_id)

        # Serialize instance
        serializer = UserSerializer(user)
        return JSONResponse(content=serializer.data)

    @router.put('/{instance_id}/', response_model=UserModel)
    @is_admin_or_owner
    async def update_user(
            request: Request,
            instance_id: PyObjectId,
            user: UserModel = Body(...),
            repository: Repository = Depends(get_user_repo)
    ):
        # Basic validation
        data = {k: v for k, v in user.dict().items() if v is not None}

        # Perform update
        instance = await repository.update(instance_id=instance_id, data=data)

        # Serialize instance
        serializer = UserSerializer(instance)
        return JSONResponse(content=serializer.data)

    @router.delete('/{instance_id}/', response_description='Delete a user')
    @is_admin_or_owner
    async def delete_user(
            request: Request,
            instance_id: PyObjectId,
            repository: Repository = Depends(get_user_repo)
    ):
        await repository.delete(instance_id)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    return router
