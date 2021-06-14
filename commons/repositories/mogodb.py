from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from commons.repositories import (
    AbstractRepository, Type, MODEL, Union
)
from commons.exceptions.instance import InstanceNotFound


class MongoDBRepository(AbstractRepository):
    collection: AsyncIOMotorCollection

    def __init__(
        self,
        db_model: Type[MODEL],
        collection: AsyncIOMotorCollection
    ):
        super().__init__(db_model)
        self.collection = collection

    async def create(self, data: dict):
        instance = await self.collection.insert_one(data)
        data.update({'_id': instance.inserted_id})
        return self.model(**data)

    async def get(
        self,
        value: Optional[Union[int, str]],
        key='_id',
        **kwargs
    ):
        instance = await self.collection.find_one({key: value})
        return self.model(**instance) if instance else None

    async def update(
            self,
            instance_id: Optional[Union[int, str]],
            model: MODEL
    ) -> MODEL:
        data = self.model(**model.dict(exclude={'id', '_id'})).dict()

        await self.collection.replace_one({"_id": instance_id}, data)
        data.update({'_id': instance_id})
        return self.model(**data)

    async def list(self, **kwargs) -> List[MODEL]:
        instances = await self.collection.find().to_list(1000)
        return instances

    async def filter(self, **kwargs):
        instances = await self.collection.find(**kwargs).to_list(1000)
        return instances

    async def delete(
            self,
            instance_id: Optional[Union[int, str]],
            key: str = '_id'
    ) -> None:
        await self.collection.delete_one({key: instance_id})

    async def get_or_404(
            self,
            value: Optional[Union[int, str]],
            key: str = '_id'
    ):
        if instance := await self.get(value, key):
            return instance

        raise InstanceNotFound()
