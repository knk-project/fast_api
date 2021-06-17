from abc import ABC, abstractmethod
from typing import Type, Optional, List, Union

from commons.models import MODEL


class AbstractRepository(ABC):
    model: Type[MODEL]

    def __init__(self, model: Type[MODEL]):
        self.model = model

    @abstractmethod
    async def create(self, model: MODEL):
        raise NotImplementedError

    @abstractmethod
    async def get(
        self,
        value: Optional[Union[int, str]],
        key: str = 'id'
    ) -> MODEL:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, instance_id: Optional[Union[int, str]],
        model: MODEL
    ) -> MODEL:
        raise NotImplementedError

    @abstractmethod
    async def list(self, **parameters) -> List[MODEL]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, instance_id: Optional[Union[int, str]]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_or_404(self, value: Optional[Union[int, str]], key: str = 'id'):
        raise NotImplementedError
