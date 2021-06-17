from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from commons.repositories import (
    AbstractRepository, Type, MODEL, Union
)
from commons.exceptions.instance import InstanceNotFound


class MongoDBRepository(AbstractRepository):
    collection: AsyncIOMotorCollection

    def __init__(self, model: Type[MODEL], collection: AsyncIOMotorCollection):
        super().__init__(model)
        self.collection = collection

    async def create(self, model: MODEL):
        return await self.collection.insert_one(model.dict(exclude={'id'}))

    async def get(self, value: Optional[Union[int, str]], key='_id') -> MODEL:
        if instance := await self.collection.find_one({key: value}):
            return self.model(**instance)

    async def update(self, instance_id: str, data: dict) -> MODEL:
        return await self.collection.update_one({"_id": instance_id},
                                                {"$set": data})

    async def list(self, **kwargs) -> List[MODEL]:
        return await self.collection.find().to_list(1000)

    async def filter(self, **kwargs) -> List[MODEL]:
        # TODO
        instances = await self.collection.find(**kwargs).to_list(1000)
        return instances

    async def delete(self, instance_id: str, key: str = '_id') -> None:
        await self.collection.delete_one({key: instance_id})

    async def get_or_404(self, value: Optional[Union[int, str]], key: str = '_id'):
        if instance := await self.get(value, key):
            return instance

        raise InstanceNotFound()
