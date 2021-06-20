from core.managers import DatabaseManager
from core.managers.mongodb import MongoDBManager


mongodb = MongoDBManager()


def get_database(manager: str = 'mongodb') -> DatabaseManager:
    if manager == 'mongodb':  # TODO add in config
        return mongodb

    return
