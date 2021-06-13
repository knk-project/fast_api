import uvicorn
import os
from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import FastAPI

from config import config
from users.router import router as user_router

app = FastAPI()

client = AsyncIOMotorClient(config.MONGODB_URL)
db = client.fast_api_db

# Set application routes
app.include_router(user_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

