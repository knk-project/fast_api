from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException
from pydantic import (Field, EmailStr, SecretStr)
from starlette import status

from commons.models import CommonModel
from roles.helpers.enum import RoleEnum


class User(CommonModel):
    email: EmailStr = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    role: RoleEnum = RoleEnum.USER
    is_active: bool = True
    last_logic: datetime = None
    hashed_password: SecretStr

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                'id': '123',
                'email': 'jdoe@example.com',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'role': 'USER',
                'is_active': True,
                'hashed_password': 'some_hashed_password',
                'last_login': '2008-09-15T15:53:00+05:00',
                'created_at': '2008-09-15T15:53:00+05:00',
                'updated_at': '2008-09-15T15:53:00+05:00',
            }
        }

    @staticmethod
    async def check_email(model, value):
        if await model.find_one({'email': value}):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[{"loc": ["email"],
                         "msg": "Email already in use.",
                         "type": "value_error"}]
            )
        return value
