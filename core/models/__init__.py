from datetime import datetime
from typing import TypeVar

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CommonModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


MODEL = TypeVar('MODEL', bound=CommonModel)
