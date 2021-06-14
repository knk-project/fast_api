from pymongo.collation import Collation

from commons.repositories.mogodb import (
    MongoDBRepository, Type, MODEL, AsyncIOMotorCollection, Optional
)
from commons.exceptions.instance import UniqueException


class UserRepository(MongoDBRepository):
    email_collation: Collation

    def __init__(
        self,
        db_model: Type[MODEL],
        collection: AsyncIOMotorCollection,
        email_collation: Optional[Collation] = None,
    ):
        super().__init__(db_model, collection)

        if email_collation:
            self.email_collation = email_collation  # pragma: no cover
        else:
            self.email_collation = Collation("en", strength=2)

        self.collection.create_index(
            "email",
            name="case_insensitive_email_index",
            collation=self.email_collation,
        )

    async def create(self, data: dict):
        if await self.get(value=data.get('email'), key='email'):
            raise UniqueException(value=data.get('email'), key='email')
        return await super().create(data)

    async def update(self, instance_id: str, model: MODEL) -> MODEL:
        instance = await self.get(value=model.email, key='email')
        if instance and str(getattr(instance, 'id', None)) != instance_id:
            raise UniqueException(value=model.email, key='email')

        return await super().update(instance_id, model)

