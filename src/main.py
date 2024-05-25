import os
from fastapi import FastAPI, Depends, Request
from fastapi.responses import Response
from fastapi_users import FastAPIUsers
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from src.auth.base_config import auth_backend
from src.auth.models import User

from src.game_session.router import router as game_session_router
from src.game_session.websocket import router as game_session_websocket_router
from src.core import Core

app = FastAPI(
    title="Kharkiv monopoly",
)

app.mount("/templates", StaticFiles(directory="templates"), name="templates")

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
app.include_router(game_session_websocket_router)

@app.middleware("http")
async def add_cache_control_header(request: Request, call_next):
    response: Response = await call_next(request)
    if request.url.path.startswith("/static"):
        response.headers["Cache-Control"] = "no-store"
    return response

@app.get("/", response_class=HTMLResponse)
async def get():
    await Core.create_tables()
    with open("templates/monopoly.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)
