from typing import List

from bson import ObjectId
from motor.motor_asyncio import (
    AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
)
from pymongo import DESCENDING

from config import config
from core.managers import DatabaseManager


class MongoDBManager(DatabaseManager):
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None
    _collection: AsyncIOMotorCollection = None

    async def connect(self, **kwargs):
        self.client = AsyncIOMotorClient(config.DB_URL)
        self.database = self.client[config.DB_NAME]

    async def disconnect(self, **kwargs):
        self.client.close()

    async def create(self, **kwargs):
        collection = self.get_collection()
        created_instance = await collection.insert_one(kwargs)
        return await collection.find_one(*[dict(_id=created_instance.inserted_id)])

    async def get(self, **kwargs):
        collection = self.get_collection()
        return await collection.find_one(*[kwargs])

    async def update(self, instance_id: ObjectId, data: dict):
        collection = self.get_collection()
        return await collection.update_one({"_id": instance_id},
                                           {"$set": data})

    async def list(self, **kwargs) -> List[dict]:
        # TODO add pagination
        collection = self.get_collection()
        return await collection.find(*[kwargs]).sort([
            ('_id', DESCENDING)
        ]).to_list(1000)

    async def delete(self, instance_id: ObjectId) -> None:
        collection = self.get_collection()
        await collection.delete_one({'_id': instance_id})

