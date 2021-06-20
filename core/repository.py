from abc import ABC, abstractmethod
from typing import Type, Optional, List, Union

from bson import ObjectId

from core.models import MODEL
from core.exceptions.instance import InstanceNotFound
from core.database import get_database
from core.managers import DatabaseManager


class Repository(ABC):
    table = None
    model: Optional[Type[MODEL]]
    _manager: DatabaseManager = None

    def __init__(self):
        self._manager = get_database()

    @abstractmethod
    async def create(self, model: MODEL):
        raise NotImplementedError

    @abstractmethod
    async def get(self, **kwargs) -> Type[MODEL]:
        raise NotImplementedError

    async def get_or_404(self, **kwargs) -> Type[MODEL]:
        if instance := await self.get(**kwargs):
            return instance

        raise InstanceNotFound()

    @abstractmethod
    async def list(self, **kwargs) -> List[Type[MODEL]]:
        raise NotImplementedError

    @abstractmethod
    async def update(
            self,
            instance_id: Optional[Union[int, str, ObjectId]],
            data: dict
    ) -> Type[MODEL]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, instance_id: Optional[Union[int, str, ObjectId]], **kwargs):
        raise NotImplementedError
