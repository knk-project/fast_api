import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI

from config import config
from users import UserApplication

# App initialization
app = FastAPI()
app.mongodb_client = None


# Initialize database client
client = AsyncIOMotorClient(config.DB_URL)
database = client[config.DB_NAME]

# Register applications.
user_service = UserApplication(database=database)
app.include_router(
    user_service.get_application_router(), prefix="/api/users", tags=["users"]
)


# Configuring uvicorn for easier management
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG_MODE,
    )

