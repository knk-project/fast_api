from pydantic import BaseSettings


class CommonConfig(BaseSettings):
    APP_NAME: str = 'FAST API test'
    DEBUG_MODE: bool = False


class DatabaseConfig(BaseSettings):
    DB_URL: str
    DB_NAME: str


class ServerConfig(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: str = "8003"


class AuthConfig(BaseSettings):
    AUTH_EXPIRE_MINUTES: int
    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str


class Config(CommonConfig, DatabaseConfig, ServerConfig, AuthConfig):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Config()
