import uvicorn
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from config import config
from core.database import get_database
from core.middleware.auth import AuthMiddleware
from users import UsersApp

# App initialization
app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=AuthMiddleware())


@app.on_event("startup")
async def startup():
    await get_database().connect()


@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()


middleware = [
    Middleware(AuthenticationMiddleware, backend=AuthMiddleware())
]

# Register applications.
user_service = UsersApp(get_database())
app.include_router(
    user_service.get_application_router(), prefix="/api/users", tags=["users"]
)

app.include_router(
    user_service.get_auth_router(), prefix="/api/auth", tags=["auth"]
)


# Configuring uvicorn for easier management
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG_MODE,
    )

