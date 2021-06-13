from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = 'ADMIN'
    DEV = 'DEV'
    USER = 'USER'
