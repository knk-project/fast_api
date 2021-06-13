from pydantic import BaseSettings
from typing import Optional


class Config(BaseSettings):
    MONGODB_URL: Optional[str] = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Config()
