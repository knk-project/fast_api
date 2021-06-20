import inspect
from abc import ABC, abstractmethod
from typing import Type, Optional, List, Union

from bson import ObjectId

from core.models import MODEL


class DatabaseManager(ABC):
    model: Type[MODEL]
    client = None
    database = None
    _collection = None

    def connect(self, **kwargs):
        raise NotImplementedError

    def disconnect(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def create(self, model: MODEL):
        raise NotImplementedError

    @abstractmethod
    async def get(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, instance_id: Optional[Union[int, str, ObjectId]], data: dict):
        raise NotImplementedError

    @abstractmethod
    async def list(self, *args, **kwargs) -> List[dict]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, instance_id: Optional[Union[int, str, ObjectId]]) -> None:
        raise NotImplementedError

    def get_collection(self):
        stack = inspect.stack()
        table_name = stack[2][0].f_locals['self'].__class__.table
        return self.database[table_name]
