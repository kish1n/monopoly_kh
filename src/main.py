import os
from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers

from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from src.auth.base_config import auth_backend
from src.auth.models import User

from src.game_session.router import router as game_session_router

from src.core import Core

app = FastAPI(
    title="Kharkiv monopoly",
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(game_session_router)

@app.get("/")
async def startup_event():
    #await Core.create_tables()
    return {"message": "rework db done"}
