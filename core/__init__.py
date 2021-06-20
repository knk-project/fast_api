from abc import ABC, abstractmethod

from fastapi import APIRouter

from core.managers import DatabaseManager


class CommonApp(ABC):
    manager: DatabaseManager = None
    router: APIRouter

    def __init__(self, database: DatabaseManager):
        self.manager = database

    @abstractmethod
    def get_application_router(self) -> APIRouter:
        raise NotImplementedError
