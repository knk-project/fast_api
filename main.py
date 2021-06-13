import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI

from config import config
from users.router import router as user_router

# App initialization
app = FastAPI()
app.mongodb_client = None


# Configuring db client
@app.on_event('startup')
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(config.DB_URL)
    app.mongodb = app.mongodb_client[config.DB_NAME]


@app.on_event('shutdown')
async def shutdown_db_client():
    app.mongodb_client.close()


# Attaching application routers
app.include_router(user_router)


# Configuring uvicorn for easier management
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG_MODE,
    )

