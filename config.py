from pydantic import BaseSettings


class CommonConfig(BaseSettings):
    APP_NAME: str = 'FAST API test'
    DEBUG_MODE: bool = False


class DatabaseConfig(BaseSettings):
    DB_URL: str
    DB_NAME: str


class ServerConfig(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: str = "8000"


class Config(CommonConfig, DatabaseConfig, ServerConfig):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Config()
