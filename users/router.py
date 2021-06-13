from typing import List
from fastapi import (APIRouter, HTTPException, Body, Request)
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from .models.user import User

router = APIRouter(tags=['Users'])


@router.post('/', response_description='Register', response_model=User)
async def create_user(request: Request, user: User = Body(...)):
    # Init model
    model = request.app.mongodb['users']

    # Basic validation
    data = jsonable_encoder(user)

    # Email validation
    await user.check_email(model=model, value=user.email)

    # Inserting user data
    new_user = await model.insert_one(data)
    assert new_user.acknowledged

    # Retrieving user data
    created_user = await model.find_one({'_id': new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.get(
    '/list/', response_description='List all users', response_model=List[User]
)
async def list_users(request: Request):
    users = await request.app.mongodb['users'].find().to_list(1000)
    return users


@router.get(
    '/{user_id}/', response_description='Get a single user', response_model=User
)
async def show_user(request: Request, user_id: str):
    if (user := await request.app.mongodb['users'].find_one({'_id': user_id})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f'User {user_id} not found')


@router.put('/{user_id}/', response_description='Update a user', response_model=User)
async def update_user(request: Request, user_id: str, user: User = Body(...)):
    # Init model
    model = request.app.mongodb['users']

    if not (existing_user := await model.find_one({'_id': user_id})):
        raise HTTPException(status_code=404, detail=f'User {user_id} not found')

    # Basic validation
    data = {k: v for k, v in user.dict().items() if v is not None}

    if not data:
        return existing_user

    # Email validation
    if user.email:
        await user.check_email(model=model, value=user.email)

    await model.update_one({'_id': user_id}, {'$set': data})
    return await model.find_one({'_id': user_id})


@router.delete('/{user_id}/', response_description='Delete a user')
async def delete_user(request: Request, user_id: str):
    delete_result = await request.app.mongodb['users'].delete_one({'_id': user_id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f'User {user_id} not found')
