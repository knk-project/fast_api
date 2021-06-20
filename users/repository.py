from datetime import datetime
from typing import Type, Optional, List

from fastapi.encoders import jsonable_encoder
from pymongo.collation import Collation

from core.exceptions.instance import UniqueException
from core.managers import DatabaseManager
from core.models import MODEL, PyObjectId
from core.repository import Repository
from users.helpers.password import get_password_hash
from users.models.user import UserModel


class User(Repository):
    model: Type[MODEL] = UserModel
    email_collation: Collation
    _database: DatabaseManager = None
    table = 'users'

    async def create(self, model: UserModel):
        # Validate email
        if await self.get(email=model.email):
            raise UniqueException(value=model.email, key='email')

        # Hash password
        model.hashed_password = get_password_hash(model.hashed_password)

        # Convert to dict
        validated_data = model.dict(exclude={'id'})

        # Store
        instance = await self._manager.create(**validated_data)

        # Return dataset as model
        return self.model(**instance)

    async def get(self, **kwargs) -> Optional[UserModel]:
        if not kwargs:
            return

        if response := await self._manager.get(**kwargs):
            return self.model(**response)

    async def update(self, instance_id: str, data: dict) -> UserModel:
        # Check if exists
        instance = await self.get_or_404(_id=instance_id)

        # Set datetime for created and updated fields
        data.update(dict(created_at=instance.created_at,
                         updated_at=datetime.now()))

        # Validate email if it set
        if email := data.get('email'):
            checker = await self._manager.get(email=email)
            if checker and checker.get('_id') != instance_id:
                raise UniqueException(value=email, key='email')

        # Hash password if it set
        if password := data.get('hashed_password'):
            data['hashed_password'] = get_password_hash(password)

        # Validate fields
        validated_data = self.validate_data(data)

        # Store
        await self._manager.update(instance_id, validated_data)

        # Return dataset as model
        return await self.get(_id=instance.id)

    def validate_data(self, data: dict) -> dict:
        model_fields = set(self.model.__fields__.keys())
        data_keys = data.keys()
        validated_data = {}

        for field in model_fields:
            if field not in data_keys:
                continue
            validated_data.update({field: data.get(field)})

        return validated_data

    async def list(self, **kwargs) -> List[UserModel]:
        jsonable = kwargs.pop('jsonable', False)
        instances = await self._manager.list(**kwargs)
        result = []
        for instance in instances:
            data = self.model(**instance)
            if jsonable:
                data = jsonable_encoder(data)
            result.append(data)

        return result

    async def delete(self, instance_id: PyObjectId, **kwargs):
        await self.get_or_404(_id=instance_id)
        return await self._manager.delete(instance_id=instance_id)


user_repository = User()


async def get_user_repo():
    return user_repository
