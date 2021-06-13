from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import (APIRouter, HTTPException, Body)
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

# from main import db
from config import config
from .models.user import User

router = APIRouter(tags=['Users'])

client = AsyncIOMotorClient(config.MONGODB_URL)
db = client.fast_api_db


@router.post('/', response_description='Register', response_model=User)
async def create_user(user: User = Body(...)):
    user = jsonable_encoder(user)
    new_user = await db['users'].insert_one(user)
    created_user = await db['users'].find_one({'_id': new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.get(
    '/list/', response_description='List all users', response_model=List[User]
)
async def list_users():
    users = await db['users'].find().to_list(1000)
    return users


@router.get(
    '/{user_id}/', response_description='Get a single user', response_model=User
)
async def show_user(user_id: str):
    if (user := await db['users'].find_one({'_id': user_id})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f'User {user_id} not found')


@router.put('/{user_id}/', response_description='Update a user', response_model=User)
async def update_user(user_id: str, user: User = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}

    if len(user) >= 1:
        update_result = await db['users'].update_one({'_id': user_id}, {'$set': user})

        if update_result.modified_count == 1:
            if (
                updated_user := await db['users'].find_one({'_id': user_id})
            ) is not None:
                return updated_user

    if (existing_user := await db['users'].find_one({'_id': user_id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f'User {user_id} not found')


@router.delete('/{user_id}/', response_description='Delete a user')
async def delete_user(user_id: str):
    delete_result = await db['users'].delete_one({'_id': user_id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f'User {user_id} not found')
