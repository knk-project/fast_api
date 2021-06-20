from fastapi import APIRouter

from core import CommonApp
from users.routers.auth import get_auth_router
from users.routers.crud import get_crud_router


class UsersApp(CommonApp):
    def get_application_router(self) -> APIRouter:
        return get_crud_router()

    def get_auth_router(self) -> APIRouter:
        return get_auth_router()
