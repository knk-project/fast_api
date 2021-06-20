from datetime import datetime

from bson import ObjectId

from pydantic import (Field, EmailStr)

from core.models import CommonModel
from roles.helpers.enum import RoleEnum


class UserModel(CommonModel):
    email: EmailStr = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    role: RoleEnum = RoleEnum.USER
    is_active: bool = True
    last_login: datetime = None
    hashed_password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
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
