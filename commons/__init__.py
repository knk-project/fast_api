from abc import ABC, abstractmethod
from typing import Type

from fastapi import APIRouter

from commons.models import MODEL
from commons.repositories import AbstractRepository


class CommonApplication(ABC):
    collection: AbstractRepository
    model: Type[MODEL]
    router: APIRouter

    @abstractmethod
    def get_application_router(self) -> APIRouter:
        raise NotImplementedError
