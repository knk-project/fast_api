from fastapi import APIRouter

from commons import CommonApplication
from users.models.user import User
from users.repository import UserRepository
from users.router import get_user_router


class UserApplication(CommonApplication):
    def __init__(self, database):
        self.collection = database["users"]
        self.repository = UserRepository(User, self.collection)
        self.model = User

    def get_application_router(self) -> APIRouter:
        return get_user_router(self.repository)
