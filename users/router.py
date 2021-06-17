from typing import List
from fastapi import (APIRouter, Body, Request)
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from commons.repositories import AbstractRepository
from users.model import User


def get_user_router(repository: AbstractRepository) -> APIRouter:
    router = APIRouter()

    @router.post('/', response_description='Register', response_model=User)
    async def create_user(user: User = Body(...)):
        new_instance = await repository.create(user)
        instance = await repository.get(new_instance.inserted_id)
        processed_data = jsonable_encoder(instance)
        processed_data.update({'id': str(processed_data.get('_id', None))})
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=processed_data)

    @router.get(
        '/list/', response_description='List all users', response_model=List[User]
    )
    async def list_users(request: Request):
        users = await repository.list()
        return users

    @router.get(
        '/{user_id}/', response_description='Get a single user', response_model=User
    )
    async def show_user(user_id: str):
        user = await repository.get_or_404(value=user_id)
        return JSONResponse(content=jsonable_encoder(user))

    @router.put('/{user_id}/', response_description='Update a user', response_model=User)
    async def update_user(request: Request, user_id: str, user: User = Body(...)):
        # Basic validation
        data = {k: v for k, v in user.dict().items() if v is not None}
        return await repository.update(instance_id=user_id, model=User(**data))

    @router.delete('/{user_id}/', response_description='Delete a user')
    async def delete_user(request: Request, user_id: str):
        raise await repository.delete(user_id)

    return router
